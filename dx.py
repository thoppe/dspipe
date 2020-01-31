from pipeline import Pipe
from pathlib import Path
import tempfile



def add2(x):
    return x+2

def compute(f0, f1):
    print(f0, f1)
    return f1

def return_input(f0, f1):
    print(f0, f1)
    return f0

def test_check_input_filenames():

    expected = ['apple.json', 'grape.json']

    with tempfile.TemporaryDirectory() as source:
        source = Path(source)

        for name in expected:
            print(source/name)
            (source / name).touch()
            
        result = Pipe(source)(return_input, 1)
        
        print(result)
        
    #expected = ["1.json", "2.json"]
    #print(result)
    #assert result == expected


test_check_input_filenames()
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
