from dataclasses import dataclass

import random
import itertools
import hashlib
from pathlib import Path
from glob import iglob

import joblib
from tqdm import tqdm
from wasabi import msg

import json
import elasticsearch
import elasticsearch.helpers


@dataclass
class Pipe:
    """
    Data science pipeline. Takes input from 'source' as an iterator or path.
    Input and generated output filename is fed into the called function.
    """

    source: str
    dest: str = None
    input_suffix: str = ""
    output_suffix: str = ""
    shuffle: bool = False
    limit: int = None
    prefilter: bool = True
    progressbar: bool = True
    autoname: bool = False

    def __post_init__(self, *args, **kwargs):
        """
        Setups up the pipe for processing. Creates an ouput directory if needed,
        shuffles data, and validiates input path or generic iterators.
        """

        self.preprocess_input()
        self.preprocess_output()

        # Shuffle the input data if requested
        if self.shuffle:
            self.F_IN = sorted(list(self.F_IN))
            random.shuffle(self.F_IN)

    def preprocess_input(self):

        # If input is a path, build an iterable from a glob
        if self.is_input_from_files:

            self.input_suffix = Path(self.input_suffix)

            # Fix the empty string case
            if self.input_suffix == Path():
                self.input_suffix = ""

            # Strip any glob characters passed
            self.input_suffix = str(self.input_suffix).lstrip("*")

            if self.prefilter:
                self.F_IN = Path(self.source).glob("*" + self.input_suffix)

                # Sort the input for fixed ordering
                self.F_IN = sorted(self.F_IN)

            else:
                # If we don't want to prefilter use an iterator glob (iglob)
                # pathlib currently doesn't support iglob
                pattern = Path(self.source) / ("*" + self.input_suffix)
                self.F_IN = iglob(str(pattern))

        # Otherwise assume source is an iterable
        else:
            self.F_IN = self.source

    def preprocess_output(self):

        # If output is a path, build a reference set of outputs
        if self.is_output_to_files:

            self.dest = Path(self.dest)

            # Create an output directory if needed
            self.dest.mkdir(parents=True, exist_ok=True)

            if not self.output_suffix:
                self.output_suffix = self.input_suffix

            self.output_suffix = str(self.output_suffix).lstrip("*")
            self.F_OUT = set(self.dest.glob("*" + self.output_suffix))

            # Conditionally filter the input
            if self.prefilter:
                self.F_IN = [
                    f for f in self.F_IN if self.get_output_file(f) not in self
                ]
        else:
            self.F_OUT = set()

    @property
    def is_input_from_files(self):
        """
        Return True if the input is a Path or string, read those files.
        """
        return isinstance(self.source, (str, Path))

    @property
    def is_output_to_files(self):
        """
        Return True if destination is a valid path.
        """
        return isinstance(self.dest, (str, Path))

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
        """
        Iterates over the valid inputs. If self.dest is a path, will perform
        an additional check to make sure it has not recently been created.
        """

        k = itertools.count()

        for f0 in self.F_IN:

            # Short circuit if limit is reached
            if self.limit and next(k) >= self.limit:
                break

            if self.is_output_to_files:
                f1 = self.get_output_file(f0)

                if f1 is not None and f1.exists() and self.prefilter:
                    msg.warn(f"Did not expect {f1} to exist, skipping")
                    continue

                yield (f0, f1)

            else:
                yield (f0,)

    def __contains__(self, f):
        """
        Check if the input is in the precompiled list.
        """
        return f in self.F_OUT

    def get_output_file(self, f0):
        """
        If 'dest' is a path, return the new output filename.
        If self.autoname is set, return an automatic name from the input.
        """

        f0 = str(f0)

        if self.autoname:
            f0 = hashlib.md5(f0.encode("utf-8")).hexdigest()

        f1 = self.dest / Path(str(f0)).stem
        return f1.with_suffix(self.output_suffix)

    def __call__(self, func, n_jobs=-1, **kwargs):
        """
        Call the input function. If n_jobs==-1 [default] run in parallel with
        full cores.
        """

        if self.progressbar:
            ITR = tqdm(self)
        else:
            ITR = self

        if n_jobs == 1:
            return [func(*args, **kwargs) for args in ITR]

        with joblib.Parallel(n_jobs) as MP:
            dfunc = joblib.delayed(func)
            return MP(dfunc(*args, **kwargs) for args in ITR)


@dataclass
class ESPipe:
    """
    Data science pipeline to process and return data to an ElasticSearch instance. 
    """

    document_index: str
    field: str = None
    progressbar: bool = True
    limit: int = None
    batch_size: int = 1000
    force: bool = False

    def __post_init__(self, *args, **kwargs):
        """
        TO DO: DOCS
        """

        self.es = elasticsearch.Elasticsearch(
            document_index=self.document_index
        )

    def _get_query(self):

        # If we are not forced, skip where a value is already present
        if self.force:
            query = {
                "query": {"match_all": {},},
            }
        else:
            query = {"query": {"bool": {"must_not": []},}}
            query["query"]["bool"]["must_not"].append(
                {"exists": {"field": self.field}}
            )

        return query

    def __iter__(self):
        """
        Iterator matches to everything right now.
        """

        query = self._get_query()
        ITR = elasticsearch.helpers.scan(
            self.es, query=query, index=self.document_index,
        )

        if self.limit:
            for k, item in zip(range(self.limit), ITR):
                item["_source"]["_id"] = item["_id"]
                yield item["_source"]
        else:
            for item in ITR:
                item["_source"]["_id"] = item["_id"]
                yield item["_source"]

    def _package(self, row, value):
        """
        Packges data for bulk inserts
        """

        rc = {}
        rc["_op_type"] = "update"
        rc["_index"] = self.document_index
        rc["_id"] = row["_id"]
        rc["doc"] = {self.field: value}
        return rc

    def clear_field(self):
        """
        Runs a destructive script removing all of the target field from the index.
        """

        upscript = {
            "script": {
                "inline": f"""ctx._source.remove("{self.field}")""",
                "lang": "painless",
            },
            "query": {"bool": {"must": [{"exists": {"field": self.field,}}]}},
        }

        self.es.update_by_query(
            index=self.document_index, body=upscript, timeout="60m"
        )

    def __call__(self, func, n_jobs=1, **kwargs):
        """
        Call the input function. If n_jobs==-1 [default] run in parallel with
        full cores.
        """

        if self.progressbar:
            query = self._get_query()
            n_hits = self.es.count(query, index=self.document_index)["count"]
            ITR = tqdm(self, total=n_hits)
        else:
            ITR = self

        if n_jobs == 1:

            batch = []
            for row in ITR:
                result = func(row, **kwargs)

                if result is None:
                    continue

                packaged_result = self._package(row, result)

                batch.append(packaged_result)

                if len(batch) >= self.batch_size:
                    res = elasticsearch.helpers.bulk(self.es, batch)
                    assert len(batch) == res[0]
                    batch = []

            if len(batch):
                res = elasticsearch.helpers.bulk(self.es, batch)
                assert len(batch) == res[0]

            return True

        if n_jobs != 1:
            raise NotImplementedError

        # If run in parallel, the entire sequence completes first ...
        """
        with joblib.Parallel(n_jobs) as MP:
            dfunc = joblib.delayed(func)

            batch = []
            for result in MP(dfunc(row, **kwargs) for row in ITR):
                if result is None:
                    continue
                batch.append(self._package
        """
