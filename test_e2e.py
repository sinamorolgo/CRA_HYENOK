import pytest #noqa

from main import run

def test_print_output(capsys):
    run()
    captured = capsys.readouterr()

    with open(r"C:\Users\User\PycharmProjects\CRA_HYENOK\results.txt") as f:
        expected = f.readlines()
    expected = ''.join(expected)
    expected = expected.replace("\n", "").replace(" ", "")
    captured = captured.out.replace("\n", "").replace(" ", "")
    assert ''.join(expected) == captured