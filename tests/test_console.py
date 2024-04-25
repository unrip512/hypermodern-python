import click.testing
import pytest


from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


"""
@pytest.fixture
def mock_request_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Pupupu",
    }
    return mock


def test_main_succeeds(runner, mock_request_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_request_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner, mock_request_get):
    runner.invoke(console.main)
   assert mock_request_get.called


"""


def test_different_line_width(runner):
    result = runner.invoke(console.main, ["1.jpg", "80"])
    assert result.exit_code == 0


def test_different_radius(runner):
    result = runner.invoke(console.main, ["2.jpg", "80"])
    assert result.exit_code == 0


def test_incomplete_circles_and_obstacles(runner):
    result = runner.invoke(console.main, ["3.jpg", "80"])
    assert result.exit_code == 0
