import pytest

from snow_instructor.arctic import app


def test_app(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    with pytest.raises(SystemExit):  # exit code is 0
        app('7')
    captured = capsys.readouterr()
    assert 'The 7-th Fibonacci number is 13' in captured.out
