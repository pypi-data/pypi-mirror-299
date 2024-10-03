import hashlib
import json
import logging
import re
from typing import Any, Callable, Literal, cast, overload
from urllib.parse import urlparse

import lancedb
import numpy as np
import pyarrow as pa
from cachetools import TTLCache
from datasets import ClassLabel, Dataset
from orcalib.client import OrcaClient
from orcalib.database import OrcaDatabase
from orcalib.exceptions import OrcaBadRequestException
from orcalib.orca_expr import OrcaExpr
from orcalib.orca_types import EnumT, EnumTypeHandle, ImageT, IntT, TextT, VectorT
from orcalib.rac.common import (
    DatasetLike,
    InputType,
    LabeledMemory,
    LabeledMemoryLookup,
)
from orcalib.rac.embedding_models import EmbeddingModel
from orcalib.rac.memoryset_analysis import LabeledMemorysetAnalysisResults
from orcalib.rac.reranker import (
    MemoryPairsDataset,
    Reranker,
    SharedEncoderReranker,
    TrainingArguments,
)
from orcalib.rac.util import (
    MemoryLookupResults,
    MemoryToInsert,
    bytes_to_pil_image,
    format_dataset,
    format_lookup_results,
    transform_data_to_dict_list,
    transform_rows_to_labeled_memories,
)
from pandas import DataFrame
from tqdm.auto import tqdm, trange

from orca_common.api_types import ColumnName, TableCreateMode

# 2 weeks in seconds
CACHE_TTL = 1.21e6


def _get_embedding_hash(q: np.ndarray) -> str:
    query_bytes = q.tobytes()
    hash_obj = hashlib.sha256()
    hash_obj.update(query_bytes)
    return hash_obj.hexdigest()


class LabeledMemoryset:  # TODO (2): metaclass this so we can split out the implementations of local and hosted into separate classes
    """
    Collection of memories with labels that are stored in an OrcaDB table and can be queried using embedding similarity search.
    """

    # TODO(p2): `adapt` method to change embedding models (i.e. re-compute embeddings for the entire dataset with a new model)

    def _init_local_db(self, model: EmbeddingModel):
        """Initializes a local (embedded!) database for storing memories and their embeddings."""
        # TODO: optimize vector index a bit incl supporting CUDA where available (lance has cuda support)

        assert isinstance(self.db, lancedb.DBConnection) and self.mode == "local"

        # first create meta table if it doesn't exist and check that the model and version match if it does
        if f"rac_meta_{self.table_name}" not in self.db.table_names():
            meta_table = self.db.create_table(
                f"rac_meta_{self.table_name}",
                schema=pa.schema(
                    [
                        pa.field("model", pa.string()),
                        pa.field("model_version", pa.string()),
                        pa.field("dummy_vector", pa.list_(pa.float32(), list_size=1)),
                    ]
                ),
            )

        meta_table = self.db.open_table(f"rac_meta_{self.table_name}")
        meta_rows = meta_table.to_pandas()

        if meta_table.count_rows() == 0:
            meta_table.add([{"model": model.value, "model_version": model.version, "dummy_vector": [1.0]}])
        elif meta_table.count_rows() > 1:
            raise ValueError(
                f"Multiple rows found for table {self.table_name}. Memoryset only supports one model version per table."
            )
        elif meta_table.count_rows() == 1 and (
            meta_rows["model"].iloc[0] != model.value or meta_rows["model_version"].iloc[0] != f"{model.version}"
        ):
            raise ValueError(
                f"Model or model version mismatch for existing Memoryset: {self.model.value}, version: {self.model.version} != {meta_rows['model'].iloc[0]}, version: {meta_rows['model_version'].iloc[0]}"
            )

        # create table if it doesn't exist
        if self.table_name not in self.db.table_names():
            _memoryset_schema = pa.schema(
                [
                    pa.field("text", pa.string()),
                    pa.field("image", pa.binary()),
                    pa.field("label", pa.int64()),
                    pa.field("label_name", pa.string()),
                    pa.field("metadata", pa.string()),
                    pa.field("memory_version", pa.int64()),
                    pa.field(
                        "embedding",
                        pa.list_(pa.float32(), list_size=model.embedding_dim),
                    ),
                ]
            )

            self.db.create_table(self.table_name, schema=_memoryset_schema, exist_ok=True)
            # TODO: add vector index (for more speed - works without it but is slow)

    def _init_hosted_db(self):
        """Initializes a hosted database (OrcaDB cloud or localhost) for storing memories and their embeddings."""

        assert self.mode == "hosted"

        # TODO(p2): nice error message if there are no valid orca credentials with a CTA to contact us to get set up
        self.db = OrcaDatabase(self.database_name)
        meta_table = self.db.create_table(
            f"rac_meta_{self.table_name}",
            model=TextT,
            model_version=TextT,
            if_table_exists=TableCreateMode.RETURN_CURR_TABLE,
        )
        meta_rows = cast(
            list[dict[ColumnName, Any]], meta_table.select().fetch()
        )  # We know the type b/c include_ids is False
        if len(meta_rows) == 0:
            meta_table.insert({"model": self.model.value, "model_version": f"{self.model.version}"})
        elif len(meta_rows) > 1:
            raise ValueError(
                f"Multiple rows found for table {self.table_name}. Memoryset only supports one model version per table."
            )
        elif len(meta_rows) == 1 and (
            meta_rows[0]["model"] != self.model.value or meta_rows[0]["model_version"] != f"{self.model.version}"
        ):
            raise ValueError(
                f"Model or model version mismatch for existing Memoryset: {self.model.value}, version: {self.model.version} != {meta_rows[0]['model']}, version: {meta_rows[0]['model_version']}"
            )

    mode: Literal["local", "hosted"]

    def __init__(
        self,
        uri: str,
        api_key: str | None = None,
        secret_key: str | None = None,
        model: EmbeddingModel = EmbeddingModel.CLIP_BASE,
        reranker: Reranker | None = None,  # TODO: make this a reranker model enum class instead
    ):
        self.original_uri = uri
        self.table = None
        self.index = None
        self.model = model
        self.reranker = reranker
        self.cache = TTLCache(maxsize=25000, ttl=CACHE_TTL)
        try:
            parsed = urlparse(uri)
        except Exception:
            raise ValueError(f"URI: {uri} is not a valid URL or path")

        if not parsed.fragment:
            self.table_name = "memories"
        else:
            table_name_match = re.fullmatch("^[a-zA-Z_]+[a-zA-Z0-9_]*$", parsed.fragment)
            if table_name_match is None:
                raise ValueError(
                    "Table name must be provided as the only URI fragment and be in the correct format (beginning with any letter or underscore followed by any combination of letters, numbers and underscores)"
                )
            else:
                self.table_name = parsed.fragment

        if parsed.scheme == "file":
            self.mode = "local"
            self.path = parsed.path
            self.db = lancedb.connect(parsed.path)
            self._init_local_db(model)
        elif parsed.scheme == "https" or parsed.scheme == "http":
            self.mode = "hosted"
            if not api_key or not secret_key:
                raise ValueError("API key and secret key must be provided for hosted databases")
            OrcaClient.set_credentials(
                api_key=api_key,
                secret_key=secret_key,
                endpoint=parsed.scheme + "://" + parsed.netloc,
            )

            if not parsed.path or parsed.path == "/":
                self.database_name = "default"
            else:
                db_name_match = re.fullmatch("^/{1}([a-zA-Z0-9_-]+)/?$", parsed.path)
                if db_name_match is None:
                    raise ValueError(
                        "Database name must be provided as the only path parameter and be in the correct format (any combination of letters, numbers, underscore, and/or dashes)"
                    )
                else:
                    self.database_name = db_name_match.group(1)
            if not api_key or not secret_key:
                raise ValueError("API key and secret key must be provided for hosted databases")

            self._init_hosted_db()
        else:
            raise ValueError(f"invalid URI scheme: {parsed.scheme} [must be one of: file, https]")

    def _insert_local(self, data: list[MemoryToInsert]):
        assert self.mode == "local" and isinstance(self.db, lancedb.DBConnection)
        self.db.open_table(self.table_name).add(data)

    def _insert_hosted(self, data: list[MemoryToInsert], label_col_type: EnumTypeHandle | None = None):
        assert self.mode == "hosted" and isinstance(self.db, OrcaDatabase)

        if not self.table:
            self.table = self.db.create_table(
                self.table_name,
                text=TextT,
                image=ImageT["PNG"],  # type: ignore -- ImageT takes a format param
                memory_version=IntT,
                label=label_col_type or IntT,
                label_name=TextT,
                metadata=TextT,
                embedding=VectorT[self.model.embedding_dim],
                if_table_exists=TableCreateMode.RETURN_CURR_TABLE,
            )
            self.index = self.db.create_vector_index(
                index_name=f"{self.table_name}_embedding_index",
                table_name=self.table_name,
                column="embedding",
                error_if_exists=False,
            )
            if self.index is None:
                logging.info(f"Using existing {self.table_name}_embedding_index")
                self.index = self.db.get_index(f"{self.table_name}_embedding_index")

        # table.insert takes in list of dicts and we must leave off image if there is no data for it or we will get an error
        data_to_insert = [cast(dict, mem) for mem in data]
        for mem in data_to_insert:
            if mem["image"] is None:
                del mem["image"]
        self.table.insert(data_to_insert)

    def insert(
        self,
        dataset: DatasetLike,
    ):
        """
        Inserts a dataset into the LabeledMemoryset database.

        For dict-like or list of dict-like datasets, there must be a `label` key and one of the following keys: `text`, `image`, or `value`.
        If there are only two keys and one is `label`, the other will be inferred to be `value`.

        For list-like datasets, the first element of each tuple must be the value and the second must be the label.

        Args:
            dataset: The dataset to insert into the LabeledMemoryset.

        Examples:
            # Example 1: Inserting a dictionary-like dataset
            >>> dataset = [{
            ...    "text": "text 1",
            ...    "label": 0
            ... }]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 2: Inserting a list-like dataset
            >>> dataset = [
            ...    ("text 1", 0),
            ...    ("text 2", 1)
            ]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 3: Inserting a Hugging Face Dataset
            from datasets import Dataset
            >>> dataset = load_dataset("frgfm/imagenette", "320px")
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)
        """
        transformed_data = transform_data_to_dict_list(dataset, self.mode)

        # Add embeddings to the transformed data
        embeddings = self.model._get_embedding(
            cast(
                list[InputType],
                [
                    mem["text"]
                    or (bytes_to_pil_image(mem["image"]) if isinstance(mem["image"], bytes) else mem["image"])
                    for mem in transformed_data
                ],
            ),
            show_progress_bar=True,
        )
        for item, embedding in zip(transformed_data, embeddings):
            item["embedding"] = embedding.tolist()

        if self.mode == "local":
            self._insert_local(transformed_data)
        elif self.mode == "hosted":
            label_col_type = (
                EnumT[dataset.features["label"].names]
                if isinstance(dataset, Dataset) and isinstance(dataset.features["label"], ClassLabel)
                else None
            )
            self._insert_hosted(transformed_data, label_col_type=label_col_type)
        else:
            raise Exception("Memoryset not initialized correctly")

    def _lookup_local(
        self, query: np.ndarray, k: int, column_oriented: bool | None = False, log: bool = False
    ) -> list[list[LabeledMemoryLookup]] | list[MemoryLookupResults]:
        assert self.mode == "local"

        def single_lookup(q: np.ndarray) -> list[LabeledMemoryLookup] | MemoryLookupResults:
            assert isinstance(self.db, lancedb.DBConnection)

            cache_key = (_get_embedding_hash(q), k)
            result = self.cache.get(cache_key, None)

            if result is None:
                result = self.db.open_table(self.table_name).search(q).with_row_id(True).limit(k).to_list()
                self.cache[cache_key] = result

                if column_oriented:
                    column_oriented_result: MemoryLookupResults = {
                        "value": [],
                        "embedding": [],
                        "memory_id": [],
                        "memory_version": [],
                        "label": [],
                        "label_name": [],
                        "metadata": [],
                        "lookup_score": [],
                    }
                    for row in result:
                        metadata = json.loads(row["metadata"]) if row["metadata"] is not None else None
                        if row["image"] is not None:
                            value = bytes_to_pil_image(row["image"])
                        else:
                            value = row["text"]
                        column_oriented_result["value"].append(value)
                        column_oriented_result["embedding"].append(np.array(row["embedding"]))
                        column_oriented_result["memory_id"].append(row["_rowid"])
                        column_oriented_result["memory_version"].append(row["memory_version"])
                        column_oriented_result["label"].append(row["label"])
                        column_oriented_result["label_name"].append(row["label_name"])
                        column_oriented_result["metadata"].append(metadata)
                        column_oriented_result["lookup_score"].append(np.dot(q, np.array(row["embedding"])))
                    return column_oriented_result

            memories = []
            for row in result:
                metadata = json.loads(row["metadata"]) if row["metadata"] is not None else None
                if row["image"] is not None:
                    value = bytes_to_pil_image(row["image"])
                else:
                    value = row["text"]
                memories.append(
                    LabeledMemoryLookup(
                        value=value,
                        embedding=np.array(row["embedding"]),
                        memory_id=row["_rowid"],
                        memory_version=row["memory_version"],
                        label=row["label"],
                        label_name=row["label_name"],
                        metadata=metadata,
                        lookup_score=np.dot(q, np.array(row["embedding"])),  # Calculate inner product
                    )
                )
            return memories

        if len(query.shape) == 1:
            return (
                cast(list[MemoryLookupResults], [single_lookup(query)])
                if column_oriented
                else cast(list[list[LabeledMemoryLookup]], [single_lookup(query)])
            )

        # For some reason, all_results: list[list[LabeledMemory]] | list[MemoryLookupResults] = [] is not typing the variable correctly
        # so we have to cast it to the correct type
        all_results = cast(list[list[LabeledMemoryLookup]] | list[MemoryLookupResults], [])
        for q in tqdm(query, disable=(not log) or (len(query) <= 100)):
            all_results.append(single_lookup(q))  # type: ignore -- we know that all return types will be the same
        return (
            cast(list[MemoryLookupResults], all_results)
            if column_oriented
            else cast(list[list[LabeledMemoryLookup]], all_results)
        )

    def _lookup_hosted(
        self,
        query: np.ndarray,
        k: int,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        column_oriented: bool | None = False,
        log: bool = False,
    ) -> list[list[LabeledMemoryLookup]] | list[MemoryLookupResults]:
        assert self.mode == "hosted" and isinstance(self.db, OrcaDatabase)
        if self.table is None:
            try:
                self.table = self.db.get_table(self.table_name)
            except ValueError:
                raise ValueError(
                    f"Table '{self.table_name}' not found in database '{self.database_name}'. Please call insert to create table and add data."
                )
        if self.index is None:
            try:
                self.index = self.db.get_index(f"{self.table_name}_embedding_index")
            except OrcaBadRequestException:
                raise ValueError(
                    f"Index '{self.table_name}_embedding_index' not found in table '{self.table_name}'. Please call insert first to create the index."
                )

        if len(query.shape) == 1:
            query_list = [(0, query)]
        else:
            query_list = [(idx, q) for idx, q in enumerate(query)]

        # save results in a list of tuples where the first element is the query index and the second element is the result
        all_results: list[tuple[int, list]] = []

        # run_ids are only set if we have enabled curate tracking in which case caching is not possible
        if not run_ids:
            for q in query_list:
                cache_key = (_get_embedding_hash(q[1]), k)
                result = self.cache.get(cache_key, None)
                if result is not None:
                    all_results.append((q[0], result))
                    query_list.remove(q)

        for i in trange(0, len(query_list), batch_size, disable=(not log) or (len(query_list) <= 5 // batch_size)):
            batch = query_list[i : i + (batch_size or len(query_list))]
            batch_list = [q[1].tolist() for q in batch]
            index_query = self.index.vector_scan(batch_list).select(
                "metadata",  # 0
                "image",  # 1
                "text",  # 2
                "label",  # 3
                "label_name",  # 4
                "memory_version",  # 5
                "$embedding",  # 6
                "$row_id",  # 7
            )
            if run_ids:
                batch_run_ids = run_ids[i : i + (batch_size or len(query_list))]
                index_query = index_query.track_with_curate(batch_run_ids, "rac_lookup")

            r = index_query.fetch(k).to_list()

            for idx, row in enumerate(r):
                cache_key = (_get_embedding_hash(batch[idx][1]), k)
                self.cache[cache_key] = row
                all_results.append((batch[idx][0], row))

        all_results.sort(key=lambda x: x[0])
        results = [format_lookup_results(r, query[r[0]], column_oriented=column_oriented) for r in all_results]
        return (
            cast(list[MemoryLookupResults], results)
            if column_oriented
            else cast(list[list[LabeledMemoryLookup]], results)
        )

    @overload
    def lookup(
        self,
        query: InputType | list[InputType] | np.ndarray,
        *,
        column_oriented: Literal[False] | None = False,
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
    ) -> list[list[LabeledMemoryLookup]]:
        pass

    @overload
    def lookup(
        self,
        query: InputType | list[InputType] | np.ndarray,
        *,
        column_oriented: Literal[True],
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
    ) -> list[MemoryLookupResults]:
        pass

    def lookup(
        self,
        query: InputType | list[InputType] | np.ndarray,
        *,
        column_oriented: bool | None = False,
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
    ) -> list[list[LabeledMemoryLookup]] | list[MemoryLookupResults]:
        """
        Retrieves the most similar memories to the query from the memoryset.

        Args:
            query: The query to retrieve memories for. Can be a single value, a list of values, or a numpy array with value embeddings.
            k: The number of memories to retrieve.
            batch_size: The number of queries to process at a time.
            run_ids: A list of run IDs to track with the lookup.
            rerank: Whether to rerank the results. If None (default), results will be reranked if a reranker is attached to the Memoryset.
            log: Whether to log the lookup process and show progress bars.

        Returns:
            A list of lists of LabeledMemoryLookups, where each inner list contains the k most similar memories to the corresponding query.

        Examples:
            # Example 1: Retrieving the most similar memory to a single example
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> query = "Apple"
            >>> memories = memoryset.lookup(query, k=1)
            [
                [
                    LabeledMemoryLookup(
                        value='Orange',
                        memory_id=12,
                        memory_version=1,
                        label=0,
                        label_name='fruit',
                        embedding=array([...], dtype=float32),
                        metadata=None,
                        lookup_score=.98,
                        reranker_score=None,
                        reranker_embedding=None
                    )
                ]
            ]
        """
        # TODO (p2): allow for some retrieval config to be passed in
        if isinstance(query, InputType):
            embedded_query = self.model._get_embedding(query)
        elif isinstance(query, list) and all(isinstance(q, InputType) for q in query):
            embedded_query = self.model._get_embedding(query)
        elif isinstance(query, np.ndarray):
            embedded_query = query
        else:
            raise ValueError("Query must be a single value, a list of values, or a numpy array")

        assert (
            len(embedded_query.shape) == 2 or len(embedded_query.shape) == 1
        ), "Query embedding is not in a valid shape"

        if len(embedded_query.shape) == 1:
            assert (
                embedded_query.shape[0] == self.model.embedding_dim
            ), f"Query embedding shape: {embedded_query.shape} does not match model embedding dimension: {self.model.embedding_dim}"
        else:
            assert (
                embedded_query.shape[1] == self.model.embedding_dim
            ), f"Query embedding shape: {embedded_query.shape} does not match model embedding dimension: {self.model.embedding_dim}"
        # Default reranking to `True` if a reranker is attached and to `False` otherwise.
        rerank = rerank or (rerank is None and self.reranker is not None)
        if rerank:
            if not self.reranker:
                raise ValueError("rerank is set to true but no reranker model has been set on this memoryset")
            k = k * self.reranker.compression
        if self.mode == "local":
            memory_lookups = self._lookup_local(embedded_query, k=k, column_oriented=column_oriented, log=log)
        elif self.mode == "hosted":
            memory_lookups = self._lookup_hosted(
                embedded_query, k=k, batch_size=batch_size, run_ids=run_ids, column_oriented=column_oriented, log=log
            )
        else:
            raise Exception("Memoryset not initialized correctly")

        # TODO: support reranking for column-oriented results
        if rerank and not column_oriented:
            assert self.reranker is not None
            # we know this is a list of list of LabeledMemoryLookups because we check that column_oriented is False
            memory_lookups = cast(list[list[LabeledMemoryLookup]], memory_lookups)
            if isinstance(query, str):
                queries_list = [query]
            else:
                if not isinstance(query, list) or not isinstance(query[0], str):
                    raise ValueError("reranking only works when passing a string as the query")
                queries_list = cast(list[str], query)
            # TODO: use cached reranker embeddings if available
            reranked_results = [
                self.reranker.rerank(q, memories=[cast(str, m.value) for m in ms], top_k=k)
                for q, ms in zip(queries_list, memory_lookups)
            ]
            return [
                [
                    LabeledMemoryLookup(
                        reranker_score=reranked_results[j].scores[idx], **memory_lookups[j][idx].__dict__
                    )
                    for idx in reranked_results[j].indices
                ]
                for j in range(len(reranked_results))
            ]
        return memory_lookups

    def get_all_memories(self) -> list[LabeledMemory]:
        """
        Retrieves all the memories of a LabeledMemoryset.

        Returns:
            A list of LabeledMemories.
        """
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            return transform_rows_to_labeled_memories(
                self.db.open_table(self.table_name).to_pandas().to_dict("records")
            )
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase) and self.table:
            return transform_rows_to_labeled_memories(
                cast(list[tuple[int, dict[ColumnName, Any]]], self.table.select().fetch(include_ids=True))
            )
        else:
            raise Exception("Memoryset not initialized correctly")

    def __len__(self):
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            return self.db.open_table(self.table_name).count_rows()
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase) and self.table:
            return self.table.count()
        else:
            raise Exception("Memoryset not initialized correctly")

    def update_embedding_model(self, new_model: EmbeddingModel, destination: "LabeledMemoryset | str | None" = None):
        """
        Updates the embedding model for the LabeledMemoryset and re-embeds all data and saves it with the new embeddings to the destination.

        Args:
            new_model: The new embedding model to use.
            destination: The destination to store the updated Memoryset.
                If None, the current Memoryset will be updated.
                If a string, a new LabeledMemoryset will be initialized with the uri given and the Memoryset will be cloned to it.
                If a LabeledMemoryset, the Memoryset will be updated to the destination LabeledMemoryset.

        Examples:
            # Example 1: Updating the embedding model for the current Memoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.update_embedding_model(EmbeddingModel.CLIP_BASE)

            # Example 2: Updating the embedding model for the current Memoryset and storing the result in a new Memoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> new_memoryset = LabeledMemoryset("file:///path/to/new_memoryset")
            >>> memoryset.update_embedding_model(EmbeddingModel.CLIP_BASE, new_memoryset)

            # Example 3: Updating the embedding model for the current Memoryset and storing the result in the same Memoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> new_memoryset = "file:///path/to/new_memoryset"
            >>> memoryset.update_embedding_model(EmbeddingModel.CLIP_BASE, new_memoryset)
        """
        # Get original Memoryset and remove all embedding data
        memoryset = self.get_all_memories()

        # If destination is None or matches self, replace the current Memoryset with the new embeddings
        if destination is None or (
            (isinstance(destination, LabeledMemoryset) and destination.original_uri == self.original_uri)
            or ((isinstance(destination, str) and destination == self.original_uri))
        ):
            destination = self
            self.model = new_model
            if isinstance(self.db, lancedb.DBConnection):
                self.db.open_table(self.table_name).delete(where="embedding != null")
            elif isinstance(self.db, OrcaDatabase):
                assert self.table
                self.table.delete(OrcaExpr(op="$NEQ", args=(self.table.embedding, False)))
            else:
                raise Exception("Memoryset not initialized correctly")
        else:
            destination = LabeledMemoryset(destination) if isinstance(destination, str) else destination
            destination.model = new_model

        destination.insert(memoryset)

    def clone(
        self,
        source: "LabeledMemoryset | str",
    ):
        """
        Clones a LabeledMemoryset from the given source LabeledMemoryset into the current LabeledMemoryset.

        Args:
            source: The LabeledMemoryset to clone. If a string, a new LabeledMemoryset will be initialized with the uri given first to be cloned from.

        Examples:
            # Example 1: Cloning a LabeledMemoryset into the current LabeledMemoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> source_memoryset = LabeledMemoryset("file:///path/to/source_memoryset")
            >>> memoryset.clone(source_memoryset)
        """
        # if the destination is the same as the source, log a warning and do nothing
        if (isinstance(source, LabeledMemoryset) and source.original_uri == self.original_uri) or (
            (isinstance(source, str) and source == self.original_uri)
        ):
            logging.info("Warning: Source and destination are the same. No data will be cloned.")
            return

        if isinstance(source, str):
            source = LabeledMemoryset(source)

        if source.mode == "local" and isinstance(source.db, lancedb.DBConnection):
            data = source.db.open_table(source.table_name).to_pandas().to_dict("records")
            self.insert(data)
        elif source.mode == "hosted" and isinstance(source.db, OrcaDatabase) and source.table:
            self.insert(cast(list[dict[ColumnName, Any]], source.table.select().fetch()))
        else:
            raise Exception("Memoryset not initialized correctly")

    def map(self, fn: Callable[[LabeledMemory], LabeledMemory], destination: "LabeledMemoryset | str | None" = None):
        """
        Maps a function over the current LabeledMemoryset and stores the result in the destination LabeledMemoryset.

        Args:
            fn: The function to map over the Memoryset.
            destination: The destination to store the result. If a string, a new LabeledMemoryset will be initialized with the uri given first.

        Examples:
            # Example 1: Mapping a function over the current LabeledMemoryset and storing the result in a new LabeledMemoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> new_memoryset = LabeledMemoryset("file:///path/to/new_memoryset")
            >>> memoryset.map(lambda x: x.example.upper(), new_memoryset)

            # Example 2: Mapping a function over the current LabeledMemoryset and storing the result in the same LabeledMemoryset
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.map(lambda x: x.example.upper(), memoryset)
        """
        original_memoryset = self.get_all_memories()

        new_memoryset = [fn(memory) for memory in original_memoryset]

        # If destination is None or matches self, replace the current Memoryset with the new memoryset values
        if destination is None or (
            (isinstance(destination, LabeledMemoryset) and destination.original_uri == self.original_uri)
            or ((isinstance(destination, str) and destination == self.original_uri))
        ):
            destination = self
            # delete all embeddings if destination is the same as self
            if isinstance(self.db, lancedb.DBConnection):
                self.db.open_table(self.table_name).delete(where="embedding != null")
            elif isinstance(self.db, OrcaDatabase):
                assert self.table
                self.table.delete(OrcaExpr(op="$NEQ", args=(self.table.embedding, False)))
            else:
                raise Exception("Memoryset not initialized correctly")

        if isinstance(destination, str):
            destination = LabeledMemoryset(destination)
        destination.insert(new_memoryset)

    def finetune_reranker(
        self,
        data: DatasetLike,
        save_dir: str = "./temp/reranker",
        num_memories: int = 9,  # TODO: unify this default with the rac mmoe_width
        training_args: TrainingArguments | None = None,
    ) -> None:
        if self.reranker is None:
            self.reranker = SharedEncoderReranker("Alibaba-NLP/gte-base-en-v1.5")
        pairs_dataset = MemoryPairsDataset(
            samples=cast(list[tuple[str, int]], format_dataset(data)),
            lookup_fn=lambda query, num_memories: [
                (cast(str, memory.value), memory.label)
                for memory in self.lookup(query, k=num_memories, column_oriented=False)[0]
            ],
            num_memories=num_memories * self.reranker.compression,
        )
        self.reranker.finetune(pairs_dataset, save_dir, training_args)
        # TODO: save reranker embeddings to database

    def drop_all_data(self, *, yes_i_am_sure: bool = False):
        """
        Drops all data in the Memoryset (use with caution!)

        Args:
            yes_i_am_sure: A boolean to confirm that you really want to delete all data.
        """
        assert yes_i_am_sure, "You must pass `yes_i_am_sure=True` to drop all data"
        self.cache.clear()
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            self.db.drop_database()
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase):
            for table_name in self.db.list_tables():
                self.db.drop_table(table_name)
        else:
            raise Exception("Memoryset not initialized correctly")

    def analyze(self, log: bool = True) -> LabeledMemorysetAnalysisResults:
        memoryset = self.get_all_memories()
        return LabeledMemorysetAnalysisResults(memoryset, lambda q, k: self.lookup(q, k=k), log)

    # TODO: filter/lazy_filter functions

    def update(self, memory_id: int, **values: Any) -> None:
        """
        Update a memory in the memoryset.

        Args:
            memory_id: The id of the memory to update.
            **values: The values to update the memory with.
        """
        raise NotImplementedError("Not implemented yet")

    def delete(self, memory_id: int) -> None:
        """
        Delete a memory from the memoryset.

        Args:
            memory_id: The id of the memory to delete.
        """
        raise NotImplementedError("Not implemented yet")

    def df(self, limit: int | None = None) -> DataFrame:
        """
        Get a pandas DataFrame representation of the memoryset.

        Returns:
            A pandas DataFrame.
        """
        return DataFrame(self.get_all_memories()[:limit])
