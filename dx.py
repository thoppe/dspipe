from pipeline import Pipe
from pathlib import Path
import tempfile
import shutil


def add2(x):
    return x+2

def idempotent(x):
    return x

def compute(f0, f1):
    print(f0, f1)
    return f1

def return_input(f0):
    print(f0)
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

        

def test_create_intermediate_file():
    """
    Makes sure output files are created.
    """

    input_file_names = ["apple.json", "grape.json", "banana.json"]
    source = create_env(input_file_names)
    dest = create_env(input_file_names[:1])

    P = Pipe(source, dest, '.json')

    # Before we call the pipe, create the second file
    (dest / input_file_names[1]).touch()

    created_files = P(touch_output, 1)
    expected = input_file_names[2:]

    assert created_files == expected

    shutil.rmtree(source)
    shutil.rmtree(dest)


test_create_intermediate_file()
exit()

def create_env(names):
    '''
    Returns a temporary directory with empty files created using names.
    '''
    source = tempfile.mkdtemp()
    
    for name in names:
        (Path(source) / name).touch()

    return Path(source)

def test_check_output_files():
    '''
    Makes sure output files are created.
    '''

    input_file_names = ['apple.json', 'grape.json']
    source = create_env(input_file_names)
    dest = create_env([])

    P = Pipe(source, dest, output_suffix='.csv')(touch_output)

    expected = ['apple.csv', 'grape.csv']
    result = sorted([x.name for x in dest.glob('*.csv')])

    assert result == expected

    shutil.rmtree(source)
    shutil.rmtree(dest)



test_check_output_files()
exit()
    
x = Pipe('foo', 'bar', '.json')(compute, 2)
result = Pipe(range(3))(add2)
print(result == list(range(2,5)))

def test_size():
    n = 17
    assert len(Pipe(range(n))) == n
'''
def test_compute_math():
    n = 23
    result = Pipe(range(n))(add2, 1)
    expected = list(range(2, n+2))

    assert(result == expected)
'''

#test_compute_math()
    
#Pipe('foo', 'bar', '*.json')(compute, 1)
#Pipe('foo', 'bar', '*.json', '*.csv')(compute, 1)
#print(len(Pipe('foo', 'bar', '.json')))
#Pipe([1,2,3], 'bar', '*.json', '*.csv')(compute, 1)
