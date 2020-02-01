![](docs/logo.jpg)

_easy to use data science pipes_

Shuffling your data from one directory into another directory is easier than before!

# On it's own, a Pipe can call a function in parallel using joblib.

``` python
from pipeline import Pipe

def add2(x):
    return x+2

result = Pipe(range(3))(add2)

# result = [2, 3, 4]
```


