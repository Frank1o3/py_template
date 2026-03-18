from io import StringIO
import sys
from unittest.mock import call, patch

import pytest

from project_name.cli import main, noice_print


class TestNoicePrint:
    def test_writes_full_text(self) -> None:
        """Every character in text must reach stdout."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            noice_print("hello", term_line=1, duration=0.0)
            output = mock_out.getvalue()
        assert "hello" in output

    def test_respects_term_line(self) -> None:
        """Cursor must be moved to the correct line."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            noice_print("x", term_line=5, duration=0.0)
            output = mock_out.getvalue()
        # ANSI move: ESC[5;0H
        assert "\033[5;0H" in output

    def test_clears_line_before_writing(self) -> None:
        """Line must be cleared before characters are written."""
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            noice_print("x", term_line=1, duration=0.0)
            output = mock_out.getvalue()
        assert "\033[2K" in output

    def test_empty_string(self) -> None:
        """Empty text should not raise or hang."""
        with patch("sys.stdout", new_callable=StringIO):
            noice_print("", term_line=1, duration=1.0)

    def test_duration_controls_delay(self) -> None:
        """sleep() delay should equal duration / len(text) per character."""
        text = "hi"
        expected_delay = 0.5 / len(text)

        with patch("time.sleep") as mock_sleep, patch("sys.stdout", new_callable=StringIO):
            noice_print(text, term_line=1, duration=0.5)

        assert mock_sleep.call_count == len(text)
        for c in mock_sleep.call_args_list:
            assert c == call(pytest.approx(expected_delay, rel=1e-6))

    def test_flushes_on_every_char(self) -> None:
        """stdout must be flushed once per character (+ once for line setup)."""
        text = "abc"
        with patch.object(sys.stdout, "write"), patch.object(sys.stdout, "flush") as mock_flush:
            noice_print(text, term_line=1, duration=0.0)
        # 1 flush for the move/clear + 1 per character
        assert mock_flush.call_count == 1 + len(text)


class TestMain:
    def test_runs_without_error(self) -> None:
        """main() should complete without raising."""
        with patch("time.sleep"), patch("sys.stdout", new_callable=StringIO):
            main()

    def test_hides_and_restores_cursor(self) -> None:
        """Cursor must be hidden at start and restored at end."""
        with patch("time.sleep"), patch("sys.stdout", new_callable=StringIO) as mock_out:
            main()
            output = mock_out.getvalue()
        assert "\033[?25l" in output  # hidden
        assert "\033[?25h" in output  # restored

    def test_restores_cursor_on_keyboard_interrupt(self) -> None:
        """Cursor must be restored even if animation is interrupted."""
        with (
            patch("project_name.__main__.noice_print", side_effect=KeyboardInterrupt),
            patch("sys.stdout", new_callable=StringIO) as mock_out,
            pytest.raises(KeyboardInterrupt),
        ):
            main()

        output = mock_out.getvalue()
        assert "\033[?25h" in output

    def test_clears_screen(self) -> None:
        """Screen must be cleared before animation starts."""
        with patch("time.sleep"), patch("sys.stdout", new_callable=StringIO) as mock_out:
            main()
            output = mock_out.getvalue()
        assert "\033[2J" in output

    def test_prints_three_lines(self) -> None:
        """main() must call noice_print exactly three times."""
        with (
            patch("sys.stdout", new_callable=StringIO),
            patch("project_name.__main__.noice_print") as mock_print,
        ):
            main()
        assert mock_print.call_count == 3

    def test_lines_use_correct_term_lines(self) -> None:
        """Each noice_print call must target a different line (1, 2, 3)."""
        with (
            patch("sys.stdout", new_callable=StringIO),
            patch("project_name.__main__.noice_print") as mock_print,
        ):
            main()
        term_lines = [c.kwargs["term_line"] for c in mock_print.call_args_list]
        assert term_lines == [1, 2, 3]
