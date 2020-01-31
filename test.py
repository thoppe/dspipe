from pipeline import Pipe


def compute(f0, f1):
    print(f0, f1)

Pipe('foo', 'bar', '.json')(compute, 1)
Pipe('foo', 'bar', '*.json')(compute, 1)
Pipe('foo', 'bar', '*.json', '*.csv')(compute, 1)

print(len(Pipe('foo', 'bar', '.json')))

#Pipe([1,2,3], 'bar', '*.json', '*.csv')(compute, 1)
