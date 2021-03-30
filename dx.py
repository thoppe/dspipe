from dspipe import Pipe, ESPipe
from pathlib import Path
import tempfile
import shutil
from tqdm import tqdm
import random
import time

def compute(doc):
    if doc['data_source'] != 'exporter':
        return None

    activity_code = doc['program'][:3]
    
    
    print(activity_code)
    return None

P = ESPipe('hhsjobs', 'derived_career_stage',
           limit=1000000, force=False)
#P.clear_field()
P(compute, 1)

exit()


#def add2(x):
#   return x+2
#print(Pipe(range(3),'foo', autoname=True)(add2))

def idempoent(x,y):
    print(x,y)
    return y

input_filenames = [1, 'apple']
result = Pipe(input_filenames, 'foo', autoname=True)(idempoent)
result = [f.name for f in result]
print(result)
exit()
#print(Pipe(['dog','cat'],'foo', autoname=True)(add2))
print(Pipe([1,'cat'],'foo', output_suffix='.pdf',autoname=False)(idempoent))


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
