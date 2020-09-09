![](docs/logo.jpg)

_easy to use data science pipes_

    pip install dspipe

Shuffling your data from one directory into another directory is easier than before!

On it's own, a Pipe can call a function in parallel using joblib.

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

This will run the pipe for every XML file in `data/xml`, create the directory `data/parsed_csv`, and give the compute function a new filename to save it to `f1` with the `.xml` replaced with `.csv`. Running the pipe with -1 (which indicate the number of cores) runs it fully in parallel. Use 1 for single threaded execution and n for a specific number of threads.

Other options and defaults for Pipe 

+ `shuffle = True` shuffle the data in the input before compute
+ `progressbar = True` turns on/off the progress bar
+ `prefilter = True` runs through the input filenames ahead of time
+ `autorename = True` turns on/off the renaming


