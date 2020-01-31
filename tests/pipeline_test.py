import pytest
from pipeline import Pipe

def add2(x):
    return x+2

def test_size():
    n = 5
    assert Pipe(range(n)) == n
    
