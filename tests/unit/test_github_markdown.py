"""Tests for GitHub markdown generation helpers."""
from datetime import datetime, timezone

import pytest

from tests.conftest import make_session, SAMPLE_STRUCTURED


class TestSessionMarkdown:
    def _get_markdown(self, structured=None, session_number=1):
        from src.writers.github_writer import _session_markdown
        session = make_session(
            started_at=datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc),
            ended_at=datetime(2026, 5, 27, 12, 30, 0, tzinfo=timezone.utc),
        )
        return _session_markdown(session, structured or SAMPLE_STRUCTURED, session_number)

    def test_contains_session_date(self):
        md = self._get_markdown()
        assert "2026-05-27" in md

    def test_contains_duration(self):
        md = self._get_markdown()
        assert "150 min" in md

    def test_contains_energy(self):
        md = self._get_markdown()
        assert "high" in md

    def test_contains_summary(self):
        md = self._get_markdown()
        assert SAMPLE_STRUCTURED["summary"] in md

    def test_contains_decisions(self):
        md = self._get_markdown()
        assert "Launch on ProductHunt" in md

    def test_decisions_section_header(self):
        md = self._get_markdown()
        assert "## ✅ Decisions" in md

    def test_contains_open_questions(self):
        md = self._get_markdown()
        assert "Do we need SOC2?" in md
        assert "## ❓ Open Questions" in md

    def test_questions_formatted_as_checkboxes(self):
        md = self._get_markdown()
        assert "- [ ] Do we need SOC2?" in md

    def test_contains_ideas(self):
        md = self._get_markdown()
        assert "Build a referral program" in md
        assert "## 💡 Ideas" in md

    def test_ideas_include_potential_level(self):
        md = self._get_markdown()
        assert "**[high]**" in md

    def test_contains_action_items(self):
        md = self._get_markdown()
        assert "Set up Stripe billing" in md
        assert "## 📌 Action Items" in md

    def test_action_items_formatted_as_checkboxes(self):
        md = self._get_markdown()
        assert "- [ ] @Bob: Set up Stripe billing" in md

    def test_context_update_section(self):
        md = self._get_markdown()
        assert "## Context Update" in md
        assert "ProductHunt launch" in md

    def test_no_decisions_section_when_empty(self):
        from src.writers.github_writer import _session_markdown
        session = make_session()
        structured = {**SAMPLE_STRUCTURED, "decisions": []}
        md = _session_markdown(session, structured, 1)
        assert "## ✅ Decisions" not in md

    def test_session_number_in_heading(self):
        md = self._get_markdown(session_number=3)
        assert "#3" in md


class TestBuildDecisionsEntry:
    def test_returns_empty_string_when_no_decisions(self):
        from src.writers.github_writer import _build_decisions_entry
        result = _build_decisions_entry({"decisions": []}, datetime.now(timezone.utc), "path.md")
        assert result == ""

    def test_includes_date_header(self):
        from src.writers.github_writer import _build_decisions_entry
        date = datetime(2026, 5, 27, tzinfo=timezone.utc)
        result = _build_decisions_entry(SAMPLE_STRUCTURED, date, "sessions/2026-05-27.md")
        assert "## 2026-05-27" in result

    def test_includes_all_decisions(self):
        from src.writers.github_writer import _build_decisions_entry
        result = _build_decisions_entry(SAMPLE_STRUCTURED, datetime.now(timezone.utc), "path.md")
        assert "Launch on ProductHunt" in result
        assert "Charge $49/seat/month" in result

    def test_includes_session_link(self):
        from src.writers.github_writer import _build_decisions_entry
        result = _build_decisions_entry(SAMPLE_STRUCTURED, datetime.now(timezone.utc), "sessions/test.md")
        assert "[Session](/sessions/test.md)" in result


class TestBuildQuestionsEntry:
    def test_returns_empty_string_when_no_questions(self):
        from src.writers.github_writer import _build_questions_entry
        result = _build_questions_entry({"open_questions": []}, datetime.now(timezone.utc))
        assert result == ""

    def test_includes_date_header(self):
        from src.writers.github_writer import _build_questions_entry
        date = datetime(2026, 5, 27, tzinfo=timezone.utc)
        result = _build_questions_entry(SAMPLE_STRUCTURED, date)
        assert "## 2026-05-27" in result

    def test_includes_all_questions(self):
        from src.writers.github_writer import _build_questions_entry
        result = _build_questions_entry(SAMPLE_STRUCTURED, datetime.now(timezone.utc))
        assert "Do we need SOC2?" in result

    def test_question_with_owner_includes_at_mention(self):
        from src.writers.github_writer import _build_questions_entry
        result = _build_questions_entry(SAMPLE_STRUCTURED, datetime.now(timezone.utc))
        assert "@Alice" in result

    def test_question_formatted_as_checkbox(self):
        from src.writers.github_writer import _build_questions_entry
        result = _build_questions_entry(SAMPLE_STRUCTURED, datetime.now(timezone.utc))
        assert "- [ ]" in result


class TestGetSessionGithubUrl:
    def test_url_format(self):
        from src.writers.github_writer import get_session_github_url
        url = get_session_github_url("sessions/2026-05-27-10-01.md")
        assert "github.com/user/startup-memory" in url
        assert "sessions/2026-05-27-10-01.md" in url
        assert "main" in url

    def test_url_starts_with_https(self):
        from src.writers.github_writer import get_session_github_url
        url = get_session_github_url("sessions/test.md")
        assert url.startswith("https://")
