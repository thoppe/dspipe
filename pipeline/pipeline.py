import random
from tqdm import tqdm
import joblib
from pathlib import Path
from wasabi import msg


class Pipeline:
    def __init__(
        self,
        load_dest,
        save_dest=None,
        old_extension=None,
        new_extension=None,
        shuffle=False,
        limit=None,
    ):

        # If the input is a Path or string, read those files.
        # Otherwise, treat as an iterator.
        self.is_input_from_files = isinstance(load_dest, (str, Path))

        # If save_dest is missing, we only need to iterate over the input
        self.is_output_to_files = save_dest is not None

        if self.has_in:
            self.load_dest = Path(load_dest)
            self.F_IN = list(self.load_dest.glob("*" + old_extension))

            # Value checks against input expression
            if not old_extension:
                err = (
                    "Must set 'old_extension' when load_dest is a file location"
                )
                raise ValueError(err)

        else:
            self.F_IN = load_dest

        if self.has_out:
            self.save_dest = Path(save_dest)
            # mkdir(save_dest)

            if not new_extension:
                err = "Must set 'new_extension' if save_dest is specified"
                raise ValueError(err)
            self.F_OUT = set(self.save_dest.glob("*" + new_extension))

            # Filter the input if we can
            self.F_IN = [
                f for f in self.F_IN if self.get_output_file(f) not in self
            ]

        else:
            self.F_OUT = set()

        # Make this a counter??
        self.k = 0
        self.limit = limit

        # Shuffle the input data if requested
        if shuffle:
            self.F_IN = sorted(list(self.F_IN))
            random.shuffle(self.F_IN)

    @property
    def has_in(self):
        return self.is_input_from_files

    @property
    def has_out(self):
        return self.is_output_to_files

    def __len__(self):
        """
        The length is the minimum size of the input iterator and the limit.
        """

        try:
            n = len(self.F_IN)
        except TypeError:
            n = None

        if not self.limit or self.limit < 0:
            return n

        return min(self.limit, n)

    def __iter__(self):

        for f0 in self.F_IN:

            if self.has_out:
                f1 = self.get_output_file(f0)

                if f1 is not None and f1.exists():
                    msg.warn(f"Did not expect {f1} to exist, skipping")
                    continue

                yield (f0, f1)

            else:
                yield (f0,)

            self.k += 1
            if self.limit and self.k >= self.limit:
                break

    def __contains__(self, x):
        return x in self.F_OUT

    def get_output_file(self, f0):

        if not self.has_out:
            return None

        f1 = self.save_dest / Path(f0).name
        return f1

    def __call__(self, func, n_jobs=-1):

        # if not len(self):
        #    return False

        if n_jobs == 1:
            for args in tqdm(self):
                func(*args)
            return True

        with joblib.Parallel(n_jobs) as MP:
            dfunc = joblib.delayed(func)
            MP(dfunc(*args) for args in tqdm(self))
