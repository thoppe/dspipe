from pipeline import Pipeline

from pathlib import Path

a = u'README.md'
b = Path(a)

print(isinstance(a, str), isinstance(b, str))
print(isinstance(a, Path), isinstance(b, Path))

def compute(f0):
    print(f0)

a = [1,2,3]

Pipeline(a)(compute)
