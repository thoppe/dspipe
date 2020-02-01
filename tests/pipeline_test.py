import pytest

import shutil
import tempfile
from pathlib import Path

from pipeline import Pipe


def add2(x):
    # Helper functions, returns input + 2
    return x + 2


def return_input(f0, *args):
    # Helper function, returns the input
    return f0


def touch_output(f0, f1):
    # Helper function, returns the output
    f1.touch()
    return f1.name


def create_env(names):
    """
    Returns a temporary directory with empty files created using names.
    """
    source = Path(tempfile.mkdtemp())

    for name in names:
        (source / name).touch()

    return source


def test_size():
    n = 17
    assert Pipe(range(n)) == n


def test_size():
    n = 17
    assert len(Pipe(range(n))) == n


def test_compute_math():
    n = 23
    result = Pipe(range(n))(add2)
    expected = list(range(2, n + 2))
    assert result == expected


def test_check_input_filenames():
    """
    Creates two input files and tests if they were feed as input.
    """

    expected = ["apple.json", "grape.json"]
    source = create_env(expected)
    result = [f0.name for f0 in Pipe(source)(return_input)]
    assert result == expected
    shutil.rmtree(source)


def test_check_input_filenames_extension():
    """
    Makes sure input extension is respected.
    """

    expected = ["apple.json", "grape.json"]

    # Add a salad (A CSV, shame!) in the directory
    source = create_env(expected + ["salad.csv"])

    P = Pipe(source, input_suffix=".json")
    result = [f0.name for f0 in P(return_input)]

    assert result == expected
    shutil.rmtree(source)


def test_check_output_files():
    """
    Makes sure output files are created.
    """

    input_file_names = ["apple.json", "grape.json"]
    source = create_env(input_file_names)
    dest = create_env([])

    P = Pipe(source, dest, output_suffix=".csv")(touch_output)

    expected = ["apple.csv", "grape.csv"]
    result = sorted([x.name for x in dest.glob("*.csv")])

    assert result == expected

    shutil.rmtree(source)
    shutil.rmtree(dest)
