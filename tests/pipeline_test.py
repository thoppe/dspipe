import pytest
import tempfile
from pathlib import Path
from pipeline import Pipe

help(Path)
exit()


def add2(x):
    return x + 2


def return_input(f0, f1):
    return f0


def test_size():
    n = 17
    assert Pipe(range(n)) == n


def test_size():
    n = 17
    assert len(Pipe(range(n))) == n


def test_compute_math():
    n = 23
    result = Pipe(range(n))(add2, 1)
    expected = list(range(2, n + 2))
    assert result == expected


def test_check_input_filenames():

    with tempfile.TemporaryDirectory() as name:
        print(name)

    result = Pipe("foo")(return_input, 1)
    expected = ["1.json", "2.json"]
    assert result == expected


# def test_input_filename():
#    pass

test_size()
