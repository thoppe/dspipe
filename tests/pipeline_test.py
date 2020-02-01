import pytest

import shutil
import tempfile
from pathlib import Path

from pipeline import Pipe


def idempotent(x):
    # Helper function, returns itself
    return x


def add2(x):
    # Helper functions, returns input + 2
    return x + 2


def return_input(f0, *args):
    # Helper function, returns the input
    return f0


def touch_output(f0, f1):
    # Helper function, returns and touches the output
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


def touch_output(f0, f1):
    # Helper function, returns the output
    f1.touch()
    return f1.name


############################################################################


def test_size():
    n = 17
    assert len(Pipe(range(n))) == n


def test_idempotent():
    # Make sure the input is returned exactly, even with multiprocessing
    n = 2000
    result = Pipe(range(n))(idempotent, -1)
    unexpected = list(range(n))
    assert unexpected == result


def test_shuffle():
    # Make sure data is shuffled, VERY unlikey for this to fail on it's own
    n = 2000
    result = Pipe(range(n), shuffle=True)(idempotent, 1)
    unexpected = list(range(n))
    assert unexpected != result


def test_limit():
    # Make sure data is properly limited.
    n, m = 37, 23
    result = Pipe(range(n), limit=10)(idempotent, 1)
    expected = list(range(m))
    assert expected != result


def test_progessbar_toggle():
    # Make sure compute still works without a progress bar
    n = 127
    result = Pipe(range(n), progressbar=False)(idempotent, 1)
    assert result == list(range(n))


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


def test_create_intermediate_file():
    """
    Makes sure output files are created.
    """

    input_file_names = ["apple.json", "grape.json", "banana.json"]
    source = create_env(input_file_names)
    dest = create_env(input_file_names[:1])

    P = Pipe(source, dest, ".json")

    # Before we call the pipe, create the second file
    (dest / input_file_names[1]).touch()

    created_files = P(touch_output, 1)
    expected = input_file_names[2:]

    assert created_files == expected

    shutil.rmtree(source)
    shutil.rmtree(dest)


def test_output_without_extension():
    source = create_env([])
    dest = create_env([])

    with pytest.raises(ValueError):
        Pipe(source, dest)
