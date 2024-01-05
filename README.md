![](docs/logo.jpg)


_easy to use data science pipes_

[![PyVersion](https://img.shields.io/pypi/pyversions/dspipe.svg)](https://img.shields.io/pypi/pyversions/dspipe.svg)
[![PyPI](https://img.shields.io/pypi/v/dspipe.svg)](https://pypi.python.org/pypi/dspipe)


    pip install dspipe

Shuffling your data from one directory into another directory is easier than before!

On it's own, a Pipe calls a function in parallel using [joblib](https://joblib.readthedocs.io/en/latest/). By default it uses all possible cores to compute:

``` python
from dspipe import Pipe

def add2(x):
    return x + 2

result = Pipe(range(3))(add2)

# result = [2, 3, 4]
```

But it can do so much more! Let's consider a more involved example, let's say you have a bunch of XML files and you'd like to parse them into clean CSVs.

``` python
from dspipe import Pipe

def compute(f0, f1):
    # Read the XML file f0
    # Turn it into a dataframe
    df.to_csv(f1)

P = Pipe("data/xml", "data/parsed_csv", input_suffix='.xml', output_suffix='.csv')

P(compute, -1)
```

This will run the pipe for every XML file in `data/xml`, create the directory `data/parsed_csv`, and give the compute function a new filename to save it to `f1` with the `.xml` replaced with `.csv`. Running the pipe with 1 as the second argument wil run single-threaded execution.

Init options for `Pipe`

``` python
    source: str
    dest: str = None
    input_suffix: str = ""
    output_suffix: str = ""
    shuffle: bool = False
    limit: int = None
    prefilter: bool = True
    progressbar: bool = True
    autoname: bool = False
    total: int = None
```

Call options for `Pipe`

``` python
def __call__(self, func, n_jobs=-1, **kwargs):
    # **kwargs are passed to the function
```