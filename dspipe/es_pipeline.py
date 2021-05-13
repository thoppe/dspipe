import elasticsearch
import elasticsearch.helpers


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
