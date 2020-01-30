#from pipeline import Pipeline
from pathlib import Path
from dataclasses import dataclass


@dataclass
class BasicPipe:
    source : str
    dest : str = None
    new_extension : str = None
    old_extension : str = None
    shuffle : bool = False
    limit : int = None

class Pipe(BasicPipe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

P = Pipe('a')
print(P)
exit()


a = u'README.md'
b = Path(a)

print(isinstance(a, str), isinstance(b, str))
print(isinstance(a, Path), isinstance(b, Path))

def compute(f0):
    print(f0)

a = [1,2,3]

Pipeline(a)(compute)
