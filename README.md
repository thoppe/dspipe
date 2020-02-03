![](docs/logo.jpg)

_easy to use data science pipes_

Shuffling your data from one directory into another directory is easier than before!

On it's own, a Pipe can call a function in parallel using joblib.

``` python
from dspipe import Pipe

def add2(x):
    return x + 2

result = Pipe(range(3))(add2)

# result = [2, 3, 4]
```

But it can do so much more! Let's consider a more involved example, let's download the posts from front page of Reddit, clean the text, and compute the sentiment.

