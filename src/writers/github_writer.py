"""Write session knowledge to GitHub as markdown files."""
from datetime import datetime, timezone

import structlog
from github import Github, GithubException
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings
from src.db.models import KnowledgeItem, Session

log = structlog.get_logger()

_gh: Github | None = None


def _get_repo():
    global _gh
    if _gh is None:
        _gh = Github(settings.github_token)
    return _gh.get_repo(settings.github_repo)


def _session_markdown(session: Session, structured: dict, session_number: int) -> str:
    date_str = session.started_at.strftime("%Y-%m-%d %H:%M UTC")
    duration = int((session.ended_at - session.started_at).total_seconds() / 60)
    energy = structured.get("energy", "medium")

    lines = [
        f"# Session {session.started_at.strftime('%Y-%m-%d')} #{session_number}",
        "",
        f"**Date:** {date_str}",
        f"**Duration:** ~{duration} min",
        f"**Energy:** {energy}",
        "",
        "## Summary",
        structured.get("summary", ""),
        "",
    ]

    decisions = structured.get("decisions", [])
    if decisions:
        lines += ["## ✅ Decisions"]
        for d in decisions:
            tags = " _" + ", ".join(d.get("tags", [])) + "_" if d.get("tags") else ""
            lines.append(f"- {d.get('text', '')}{tags}")
        lines.append("")

    questions = structured.get("open_questions", [])
    if questions:
        lines += ["## ❓ Open Questions"]
        for q in questions:
            owner = f" — @{q['owner']}" if q.get("owner") else ""
            lines.append(f"- [ ] {q.get('text', '')}{owner}")
        lines.append("")

    ideas = structured.get("ideas", [])
    if ideas:
        lines += ["## 💡 Ideas"]
        for idea in ideas:
            potential = f"**[{idea.get('potential', 'medium')}]** " if idea.get("potential") else ""
            tags = " _" + ", ".join(idea.get("tags", [])) + "_" if idea.get("tags") else ""
            lines.append(f"- {potential}{idea.get('text', '')}{tags}")
        lines.append("")

    actions = structured.get("action_items", [])
    if actions:
        lines += ["## 📌 Action Items"]
        for a in actions:
            owner = f"@{a['owner']}: " if a.get("owner") else ""
            lines.append(f"- [ ] {owner}{a.get('text', '')}")
        lines.append("")

    context_update = structured.get("context_update", "")
    if context_update:
        lines += ["## Context Update", context_update, ""]

    return "\n".join(lines)


def _build_decisions_entry(structured: dict, session_date: datetime, session_file_path: str) -> str:
    decisions = structured.get("decisions", [])
    if not decisions:
        return ""
    date_str = session_date.strftime("%Y-%m-%d")
    lines = [f"\n## {date_str}"]
    for d in decisions:
        lines.append(f"- {d.get('text', '')} — [Session](/{session_file_path})")
    return "\n".join(lines)


def _build_questions_entry(structured: dict, session_date: datetime) -> str:
    questions = structured.get("open_questions", [])
    if not questions:
        return ""
    date_str = session_date.strftime("%Y-%m-%d")
    lines = [f"\n## {date_str}"]
    for q in questions:
        owner = f" — @{q['owner']}" if q.get("owner") else ""
        lines.append(f"- [ ] {q.get('text', '')}{owner}")
    return "\n".join(lines)


def _get_or_create_file(repo, path: str, default_content: str) -> tuple[str, str | None]:
    """Get file content and sha, or return defaults if file doesn't exist."""
    try:
        file = repo.get_contents(path, ref=settings.github_branch)
        return file.decoded_content.decode("utf-8"), file.sha
    except GithubException as e:
        if e.status == 404:
            return default_content, None
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30))
async def write_session_to_github(
    session: Session,
    structured: dict,
    session_number: int,
    startup_context: str,
    all_open_questions: list[KnowledgeItem],
    all_open_actions: list[KnowledgeItem],
    key_decisions: list[dict],
) -> str:
    """Commit all session files to GitHub. Returns the session file path."""
    import asyncio

    loop = asyncio.get_event_loop()
    repo = await loop.run_in_executor(None, _get_repo)

    session_date = session.started_at
    session_file_path = f"sessions/{session_date.strftime('%Y-%m-%d')}-{session_date.strftime('%H')}-{session_number:02d}.md"
    session_md = _session_markdown(session, structured, session_number)

    commit_files: list[tuple[str, str]] = [(session_file_path, session_md)]

    # Accumulative decisions file — blocking HTTP, must run in executor
    decisions_default = "# All Decisions\n"
    decisions_content, _ = await loop.run_in_executor(
        None, _get_or_create_file, repo, "decisions/all-decisions.md", decisions_default
    )
    entry = _build_decisions_entry(structured, session_date, session_file_path)
    if entry:
        commit_files.append(("decisions/all-decisions.md", decisions_content + entry))

    # Accumulative open questions file — blocking HTTP, must run in executor
    questions_default = "# Open Questions\n"
    questions_content, _ = await loop.run_in_executor(
        None, _get_or_create_file, repo, "open-questions/open-questions.md", questions_default
    )
    q_entry = _build_questions_entry(structured, session_date)
    if q_entry:
        commit_files.append(("open-questions/open-questions.md", questions_content + q_entry))

    # STARTUP_CONTEXT.md — full regeneration
    commit_files.append(("STARTUP_CONTEXT.md", startup_context))

    # Build commit message
    decisions_count = len(structured.get("decisions", []))
    questions_count = len(structured.get("open_questions", []))
    actions_count = len(structured.get("action_items", []))
    summary_first = structured.get("summary", "")[:80].replace("\n", " ")
    commit_message = (
        f"session {session_date.strftime('%Y-%m-%d')}: {summary_first} "
        f"| {decisions_count}d {questions_count}q {actions_count}a"
    )

    # Create a single commit with all files — blocking HTTP
    await loop.run_in_executor(None, _commit_files, repo, commit_files, commit_message)

    log.info("github_commit_done", path=session_file_path)
    return session_file_path


def _commit_files(repo, files: list[tuple[str, str]], message: str) -> None:
    """Create a single git commit with multiple file changes."""
    branch_ref = repo.get_git_ref(f"heads/{settings.github_branch}")
    branch_sha = branch_ref.object.sha
    base_tree = repo.get_git_commit(branch_sha).tree

    new_blobs = []
    for path, content in files:
        blob = repo.create_git_blob(content, "utf-8")
        new_blobs.append(
            {"path": path, "mode": "100644", "type": "blob", "sha": blob.sha}
        )

    new_tree = repo.create_git_tree(new_blobs, base_tree)
    author = repo.get_git_commit(branch_sha).author
    commit = repo.create_git_commit(
        message=message,
        tree=new_tree,
        parents=[repo.get_git_commit(branch_sha)],
    )
    branch_ref.edit(commit.sha)


def get_session_github_url(session_file_path: str) -> str:
    return f"https://github.com/{settings.github_repo}/blob/{settings.github_branch}/{session_file_path}"
