"""Tests for session grouping logic — no external dependencies."""
from datetime import datetime, timedelta, timezone

import pytest

from tests.conftest import make_message


def _msg(msg_id: int, offset_minutes: int, **kwargs):
    base = datetime(2026, 5, 27, 10, 0, 0, tzinfo=timezone.utc)
    return make_message(
        msg_id=msg_id,
        date=base + timedelta(minutes=offset_minutes),
        **kwargs,
    )


class TestBuildSessions:
    def test_empty_list_returns_empty(self):
        from src.processors.session_builder import build_sessions
        assert build_sessions([]) == []

    def test_single_message_creates_one_session(self):
        from src.processors.session_builder import build_sessions
        msgs = [_msg(1, 0)]
        sessions = build_sessions(msgs)
        assert len(sessions) == 1
        assert len(sessions[0].messages) == 1

    def test_continuous_messages_form_one_session(self):
        from src.processors.session_builder import build_sessions
        msgs = [_msg(i, i * 10) for i in range(5)]  # 10-min gaps < 120-min threshold
        sessions = build_sessions(msgs)
        assert len(sessions) == 1
        assert len(sessions[0].messages) == 5

    def test_gap_exceeding_threshold_splits_sessions(self):
        from src.processors.session_builder import build_sessions
        # Gap of 130 minutes exceeds the 120-minute default
        msgs = [_msg(1, 0), _msg(2, 130)]
        sessions = build_sessions(msgs)
        assert len(sessions) == 2
        assert sessions[0].messages[0].msg_id == 1
        assert sessions[1].messages[0].msg_id == 2

    def test_exactly_at_threshold_stays_in_same_session(self):
        from src.processors.session_builder import build_sessions
        msgs = [_msg(1, 0), _msg(2, 120)]  # exactly 120 min — NOT > threshold
        sessions = build_sessions(msgs)
        assert len(sessions) == 1

    def test_multiple_sessions_correct_start_end_times(self):
        from src.processors.session_builder import build_sessions
        msgs = [_msg(1, 0), _msg(2, 10), _msg(3, 200), _msg(4, 210)]
        sessions = build_sessions(msgs)
        assert len(sessions) == 2
        assert sessions[0].started_at == msgs[0].date
        assert sessions[0].ended_at == msgs[1].date
        assert sessions[1].started_at == msgs[2].date
        assert sessions[1].ended_at == msgs[3].date

    def test_three_sessions(self):
        from src.processors.session_builder import build_sessions
        msgs = [
            _msg(1, 0), _msg(2, 5),         # session 1
            _msg(3, 200), _msg(4, 205),      # session 2
            _msg(5, 400), _msg(6, 405),      # session 3
        ]
        sessions = build_sessions(msgs)
        assert len(sessions) == 3


class TestMergeAlbums:
    def test_messages_without_grouped_id_preserved_as_is(self):
        from src.processors.session_builder import merge_albums
        msgs = [_msg(1, 0), _msg(2, 5), _msg(3, 10)]
        result = merge_albums(msgs)
        assert len(result) == 3
        assert all(not isinstance(item, list) for item in result)

    def test_messages_with_same_grouped_id_merged(self):
        from src.processors.session_builder import merge_albums
        msgs = [
            _msg(1, 0, grouped_id=100),
            _msg(2, 1, grouped_id=100),
            _msg(3, 2, grouped_id=100),
        ]
        result = merge_albums(msgs)
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == 3

    def test_mixed_album_and_regular_messages(self):
        from src.processors.session_builder import merge_albums
        msgs = [
            _msg(1, 0),
            _msg(2, 1, grouped_id=200),
            _msg(3, 2, grouped_id=200),
            _msg(4, 3),
        ]
        result = merge_albums(msgs)
        assert len(result) == 3  # msg1, [msg2,msg3], msg4

    def test_two_different_albums(self):
        from src.processors.session_builder import merge_albums
        msgs = [
            _msg(1, 0, grouped_id=100),
            _msg(2, 1, grouped_id=100),
            _msg(3, 5, grouped_id=200),
            _msg(4, 6, grouped_id=200),
        ]
        result = merge_albums(msgs)
        assert len(result) == 2
        assert all(isinstance(item, list) for item in result)

    def test_result_is_sorted_chronologically(self):
        from src.processors.session_builder import merge_albums
        msgs = [
            _msg(1, 0),
            _msg(2, 2, grouped_id=100),
            _msg(3, 3, grouped_id=100),
            _msg(4, 5),
        ]
        result = merge_albums(msgs)
        # First item should be earliest (msg 1 at offset 0)
        first = result[0]
        last = result[-1]
        assert (first if not isinstance(first, list) else first[0]).msg_id == 1
        assert (last if not isinstance(last, list) else last[0]).msg_id == 4


class TestBuildReplyTree:
    def test_no_replies_returns_empty_tree(self):
        from src.processors.session_builder import build_reply_tree
        msgs = [_msg(1, 0), _msg(2, 5)]
        tree = build_reply_tree(msgs)
        assert tree == {}

    def test_single_reply_mapped_to_parent(self):
        from src.processors.session_builder import build_reply_tree
        msgs = [_msg(1, 0), _msg(2, 5, reply_to_msg_id=1)]
        tree = build_reply_tree(msgs)
        assert 1 in tree
        assert len(tree[1]) == 1
        assert tree[1][0].msg_id == 2

    def test_multiple_replies_to_same_parent(self):
        from src.processors.session_builder import build_reply_tree
        msgs = [
            _msg(1, 0),
            _msg(2, 5, reply_to_msg_id=1),
            _msg(3, 10, reply_to_msg_id=1),
        ]
        tree = build_reply_tree(msgs)
        assert len(tree[1]) == 2

    def test_nested_replies(self):
        from src.processors.session_builder import build_reply_tree
        msgs = [
            _msg(1, 0),
            _msg(2, 5, reply_to_msg_id=1),
            _msg(3, 10, reply_to_msg_id=2),
        ]
        tree = build_reply_tree(msgs)
        assert 1 in tree
        assert 2 in tree
        assert 3 not in tree


class TestFormatConversation:
    def test_basic_text_messages(self):
        from src.processors.session_builder import format_conversation
        msgs = [
            _msg(1, 0, text="Hello", author_name="Alice"),
            _msg(2, 5, text="Hi there", author_name="Bob"),
        ]
        result = format_conversation(msgs)
        assert "Alice" in result
        assert "Bob" in result
        assert "Hello" in result
        assert "Hi there" in result

    def test_time_format_included(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="Hello")]
        result = format_conversation(msgs)
        assert "[10:00]" in result

    def test_fallback_author_name_when_missing(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, author_name="", author_id=42, text="test")]
        result = format_conversation(msgs)
        assert "user_42" in result

    def test_voice_transcription_included(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="", transcription="Voice content here")]
        result = format_conversation(msgs)
        assert "Voice: Voice content here" in result

    def test_ocr_text_included(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="", ocr_text="Text from image")]
        result = format_conversation(msgs)
        assert "Image text: Text from image" in result

    def test_link_metadata_included(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="", link_metadata={"title": "Hacker News", "description": "Tech news"})]
        result = format_conversation(msgs)
        assert "Hacker News" in result
        assert "Tech news" in result

    def test_media_only_message_shows_placeholder(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="", has_media=True)]
        result = format_conversation(msgs)
        assert "[media]" in result

    def test_multiple_content_parts_joined_with_pipe(self):
        from src.processors.session_builder import format_conversation
        msgs = [_msg(1, 0, text="Hello", transcription="and voice")]
        result = format_conversation(msgs)
        assert " | " in result

    def test_empty_message_list(self):
        from src.processors.session_builder import format_conversation
        assert format_conversation([]) == ""
