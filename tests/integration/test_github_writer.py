"""Tests for GitHub writer — fully mocked PyGithub."""
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import make_session, SAMPLE_STRUCTURED


def _make_github_repo():
    repo = MagicMock()

    # Mock branch ref
    branch_ref = MagicMock()
    branch_ref.object.sha = "abc123"
    repo.get_git_ref.return_value = branch_ref

    # Mock commit
    commit = MagicMock()
    commit.tree.sha = "tree123"
    commit.author = MagicMock()
    repo.get_git_commit.return_value = commit

    # Mock blob
    blob = MagicMock()
    blob.sha = "blob123"
    repo.create_git_blob.return_value = blob

    # Mock tree
    new_tree = MagicMock()
    repo.create_git_tree.return_value = new_tree

    # Mock new commit
    new_commit = MagicMock()
    new_commit.sha = "newcommit123"
    repo.create_git_commit.return_value = new_commit

    # Mock file contents (for _get_or_create_file)
    file_content = MagicMock()
    file_content.decoded_content = b"# All Decisions\n"
    file_content.sha = "filesh123"
    repo.get_contents.return_value = file_content

    return repo


class TestGetOrCreateFile:
    def test_returns_existing_file_content(self):
        from src.writers.github_writer import _get_or_create_file
        repo = MagicMock()
        file = MagicMock()
        file.decoded_content = b"existing content"
        file.sha = "sha123"
        repo.get_contents.return_value = file

        content, sha = _get_or_create_file(repo, "path/file.md", "default")
        assert content == "existing content"
        assert sha == "sha123"

    def test_returns_default_when_file_not_found(self):
        from src.writers.github_writer import _get_or_create_file
        from github import GithubException
        repo = MagicMock()
        repo.get_contents.side_effect = GithubException(404, "not found", {})

        content, sha = _get_or_create_file(repo, "path/file.md", "default content")
        assert content == "default content"
        assert sha is None

    def test_propagates_non_404_exception(self):
        from src.writers.github_writer import _get_or_create_file
        from github import GithubException
        repo = MagicMock()
        repo.get_contents.side_effect = GithubException(500, "server error", {})

        with pytest.raises(GithubException):
            _get_or_create_file(repo, "path/file.md", "default")


class TestCommitFiles:
    def test_creates_blobs_for_each_file(self):
        from src.writers.github_writer import _commit_files
        repo = _make_github_repo()
        files = [("path1.md", "content1"), ("path2.md", "content2")]

        _commit_files(repo, files, "test commit")

        assert repo.create_git_blob.call_count == 2

    def test_creates_tree_with_correct_file_modes(self):
        from src.writers.github_writer import _commit_files
        repo = _make_github_repo()
        files = [("sessions/test.md", "content")]

        _commit_files(repo, files, "commit msg")

        tree_call = repo.create_git_tree.call_args
        items = tree_call.args[0]
        assert items[0]["mode"] == "100644"
        assert items[0]["type"] == "blob"

    def test_creates_commit_with_given_message(self):
        from src.writers.github_writer import _commit_files
        repo = _make_github_repo()

        _commit_files(repo, [("file.md", "content")], "my commit message")

        commit_call = repo.create_git_commit.call_args
        assert commit_call.kwargs["message"] == "my commit message"

    def test_updates_branch_ref_to_new_commit(self):
        from src.writers.github_writer import _commit_files
        repo = _make_github_repo()

        _commit_files(repo, [("file.md", "content")], "msg")

        repo.get_git_ref.return_value.edit.assert_called_once_with("newcommit123")


class TestWriteSessionToGithub:
    async def test_returns_session_file_path(self):
        from src.writers.github_writer import write_session_to_github
        session = make_session(
            started_at=datetime(2026, 5, 27, 10, 30, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 12, 0, tzinfo=timezone.utc),
        )
        repo = _make_github_repo()

        with patch("src.writers.github_writer._get_repo", return_value=repo):
            with patch("asyncio.get_event_loop") as mock_loop:
                mock_loop.return_value.run_in_executor = AsyncMock(
                    side_effect=lambda exc, fn, *args: fn(*args) if fn != _get_repo_fn else repo
                )
                # Patch _commit_files directly to avoid executor
                with patch("src.writers.github_writer._commit_files"):
                    with patch("src.writers.github_writer._get_repo", return_value=repo):
                        result = await write_session_to_github(
                            session=session,
                            structured=SAMPLE_STRUCTURED,
                            session_number=1,
                            startup_context="# Context\nTest",
                            all_open_questions=[],
                            all_open_actions=[],
                            key_decisions=[],
                        )

        assert "sessions/2026-05-27-10-01.md" == result

    async def test_commit_message_contains_session_date(self):
        from src.writers.github_writer import write_session_to_github
        session = make_session(
            started_at=datetime(2026, 5, 27, 10, 0, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 12, 0, tzinfo=timezone.utc),
        )
        repo = _make_github_repo()
        commit_messages = []

        def capture_commit_files(repo, files, message):
            commit_messages.append(message)

        with patch("src.writers.github_writer._get_repo", return_value=repo):
            with patch("src.writers.github_writer._commit_files", side_effect=capture_commit_files):
                result = await write_session_to_github(
                    session=session,
                    structured=SAMPLE_STRUCTURED,
                    session_number=1,
                    startup_context="context",
                    all_open_questions=[],
                    all_open_actions=[],
                    key_decisions=[],
                )

        assert len(commit_messages) == 1
        assert "2026-05-27" in commit_messages[0]
        assert "2d" in commit_messages[0]  # 2 decisions
        assert "1q" in commit_messages[0]  # 1 question
        assert "1a" in commit_messages[0]  # 1 action item

    async def test_startup_context_included_in_commit(self):
        from src.writers.github_writer import write_session_to_github
        session = make_session()
        repo = _make_github_repo()
        committed_files = []

        def capture_commit_files(repo, files, message):
            committed_files.extend(files)

        with patch("src.writers.github_writer._get_repo", return_value=repo):
            with patch("src.writers.github_writer._commit_files", side_effect=capture_commit_files):
                await write_session_to_github(
                    session=session,
                    structured=SAMPLE_STRUCTURED,
                    session_number=1,
                    startup_context="# Startup Context\nCurrent state",
                    all_open_questions=[],
                    all_open_actions=[],
                    key_decisions=[],
                )

        file_paths = [f[0] for f in committed_files]
        assert "STARTUP_CONTEXT.md" in file_paths

        startup_content = next(f[1] for f in committed_files if f[0] == "STARTUP_CONTEXT.md")
        assert "# Startup Context" in startup_content


def _get_repo_fn():
    pass
