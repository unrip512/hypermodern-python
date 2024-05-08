"""Test cases for the console module."""

import pytest
from click.testing import CliRunner
from hypermodern_python import console


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_different_line_width(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main, ["1.jpg", "80"])
    assert result.exit_code == 0


def test_different_radius(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main, ["2.jpg", "80"])
    assert result.exit_code == 0


def test_incomplete_circles_and_obstacles(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main, ["3.jpg", "80"])
    assert result.exit_code == 0
