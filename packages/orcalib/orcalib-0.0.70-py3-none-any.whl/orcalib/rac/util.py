import io
import json
import logging
import random
from collections import defaultdict
from collections.abc import Mapping
from typing import Any, Literal, TypedDict, cast

import numpy as np
import pandas as pd
from datasets import Dataset, DatasetDict
from PIL import Image
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset
from tqdm.auto import tqdm

from orcalib import ColumnName
from orcalib.rac.common import (
    DatasetLike,
    InputType,
    LabeledMemory,
    LabeledMemoryLookup,
)

logger = logging.getLogger(__name__)


def pil_image_to_bytes(image: Image.Image, format: str = "JPEG") -> bytes:
    byte_array = io.BytesIO()
    if format == "JPEG":
        image = image.convert("RGB")
    image.save(byte_array, format=format)
    byte_data = byte_array.getvalue()
    return byte_data


# Convert Bytes to PIL Image
def bytes_to_pil_image(byte_data: bytes) -> Image.Image:
    byte_array = io.BytesIO(byte_data)
    image = Image.open(byte_array)
    return image


def format_dataset(dataset: DatasetLike, log: bool = False) -> list[tuple[InputType, int]]:
    if isinstance(dataset, pd.DataFrame):
        return format_pandas_dataframe(dataset, log)
    elif isinstance(dataset, Dataset):
        return format_huggingface_dataset(dataset, log)
    elif isinstance(dataset, TorchDataset):
        return format_pytorch_dataset(dataset, log)
    elif isinstance(dataset, TorchDataLoader):
        return format_pytorch_dataloader(dataset, log)
    elif isinstance(dataset, dict):
        return format_list_of_dicts([dataset], log)
    elif isinstance(dataset, LabeledMemory):
        return format_memories([dataset], log)
    elif isinstance(dataset, list):
        if isinstance(dataset[0], dict):
            return format_list_of_dicts(cast(list[dict], dataset), log)
        elif isinstance(dataset[0], LabeledMemory):
            return format_memories(cast(list[LabeledMemory], dataset), log)
        elif isinstance(dataset[0], tuple) and len(dataset[0]) == 2:
            # Handle list of tuples: no op.
            return cast(list[tuple[InputType, int]], dataset)
        else:
            raise TypeError(f"Unsupported dataset format: {type(dataset[0])}")
    else:
        raise TypeError("Unsupported dataset format")


def format_memories(dataset: list[LabeledMemory], log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    for row in tqdm(dataset, total=len(dataset), desc="Formatting Memory Fragments", disable=not log):
        formatted_dataset.append((row.value, row.label))
    return formatted_dataset


def format_list_of_dicts(dataset: list[dict], log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    for row in tqdm(dataset, total=len(dataset), desc="Formatting List of Dicts", disable=not log):
        if "value" in row and "label" in row:
            value = row["value"]
            label = row["label"]
        elif "image" in row and "label" in row:
            value = row["image"]
            label = row["label"]
        elif "text" in row and "label" in row:
            value = row["text"]
            label = row["label"]
        elif "label" in row and len(row) == 2:
            label = row["label"]
            del row["label"]
            value = row[[row.keys()][0]]
        else:
            raise TypeError("List of dicts does not contain 'value' and 'label' columns")

        formatted_dataset.append((value, label))
    return formatted_dataset


def format_pandas_dataframe(dataset: pd.DataFrame, log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    for _, row in tqdm(dataset.iterrows(), total=len(dataset), desc="Formatting Pandas DataFrame", disable=not log):
        if "value" in row and "label" in row:
            value = cast(InputType, row["value"])
            label = cast(int, row["label"])
        elif "image" in row and "label" in row:
            value = cast(InputType, row["image"])
            label = cast(int, row["label"])
        elif "text" in row and "label" in row:
            value = cast(InputType, row["text"])
            label = cast(int, row["label"])
        elif "label" in row and row.shape[0] == 2:
            value = cast(InputType, row.drop("label").iloc[0])
            label = cast(int, row["label"])
        else:
            raise TypeError("DataFrame does not contain 'value' and 'label' columns")

        formatted_dataset.append((value, label))
    return formatted_dataset


def format_huggingface_dataset(dataset: Dataset, log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    # Check if the dataset supports string-based indexing
    if all(isinstance(row, dict) for row in dataset):
        for row in tqdm(dataset, total=len(dataset), desc="Formatting Huggingface Dataset", disable=not log):
            if "value" in row and "label" in row and isinstance(row, dict):
                value = row["value"]
                label = row["label"]
            elif "image" in row and "label" in row and isinstance(row, dict):
                value = row["image"]
                label = row["label"]
            elif "text" in row and "label" in row and isinstance(row, dict):
                value = row["text"]
                label = row["label"]
            elif "label" in row and isinstance(row, dict) and len(row.keys()) == 2:
                label = row["label"]
                value = [v for k, v in row.items() if k != "label"][0]
            else:
                raise TypeError("Dataset does not contain 'value' and 'label' columns")

            formatted_dataset.append((value, label))
    else:
        # Handle the case where the dataset does not support string-based indexing
        raise TypeError("Dataset does not support string-based indexing")
    return formatted_dataset


def format_pytorch_dataset(dataset: TorchDataset, log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    dataset_list = [item for item in dataset]
    for row in tqdm(dataset_list, total=len(dataset_list), desc="Formatting PyTorch Dataset", disable=not log):
        if "value" in row and "label" in row:
            value = row["value"]
            label = row["label"]
        elif "image" in row and "label" in row:
            value = row["image"]
            label = row["label"]
        elif "text" in row and "label" in row:
            value = row["text"]
            label = row["label"]
        elif "label" in row and "value" not in row and len(row) == 2:
            label = row["label"]
            value = [v for k, v in row.items() if k != "label"][0]
        else:
            raise TypeError("PyTorch Dataset does not contain 'value' and 'label' columns")

        formatted_dataset.append((value, label))
    return formatted_dataset


def format_pytorch_dataloader(dataset: TorchDataLoader, log: bool) -> list[tuple[InputType, int]]:
    formatted_dataset: list[tuple[InputType, int]] = []
    for row in tqdm(dataset, total=len(dataset), desc="Formatting PyTorch Dataloader", disable=not log):
        if "value" in row and "label" in row:
            value = row["value"][0]
            label = row["label"].item()
        elif "image" in row and "label" in row:
            value = row["image"][0]
            label = row["label"].item()
        elif "text" in row and "label" in row:
            value = row["text"][0]
            label = row["label"].item()
        elif "label" in row and "value" not in row and len(row) == 2:
            label = row["label"].item()
            value = [v for k, v in row.items() if k != "label"][0][0]
        else:
            raise TypeError("PyTorch Dataloader does not contain 'value' and 'label' columns")

        formatted_dataset.append((value, label))
    return formatted_dataset


def drift_classes(dataset: DatasetDict | Dataset, drift_ratios: dict[int, float]) -> DatasetDict | Dataset:
    """
    Modify a balanced Huggingface dataset into an unequal distribution.

    Args:
        dataset: The Huggingface dataset (assumed balanced).
        drift_ratios: A dictionary where keys are class ints, and values are the desired proportion
            of samples to retain (e.g., {0: 0.5, 1: 0.2, 2: 1.0}). If a key is missing it will be unchanged.

    Returns:
        A new dataset with drifted class distributions.
    """

    def drift_dataset(dataset: Dataset, drift_ratios: dict) -> Dataset:
        # Define a generator that yields downsampled items directly
        def downsampled_generator(dataset):
            class_groups = defaultdict(list)
            for item in dataset:
                label = item["label"]
                class_groups[label].append(item)

                # Once a class reaches the target size, yield the downsampled items
                if len(class_groups[label]) > 1000:  # Arbitrary chunk size to avoid too large memory usage
                    yield from downsample_class(label, class_groups[label], drift_ratios)
                    class_groups[label] = []  # Clear the class group to free memory

            # Process any remaining samples for each class
            for label, group in class_groups.items():
                yield from downsample_class(label, group, drift_ratios)

        def downsample_class(label, group, drift_ratios):
            retain_count = int(len(group) * drift_ratios.get(label, 1.0))
            return random.sample(group, retain_count)

        # Use the generator to create the final dataset
        final = Dataset.from_generator(lambda: downsampled_generator(dataset))
        assert isinstance(final, Dataset)
        return final

    def drift_dataset_dict(input_dataset: DatasetDict, drift_ratios: dict) -> DatasetDict:
        drifted_datasets_dict = {}
        for dataset_name, dataset in input_dataset.items():
            # Create a new datasetDict from the drifted samples
            drifted_dataset = drift_dataset(dataset, drift_ratios)
            drifted_datasets_dict[dataset_name] = drifted_dataset
        return DatasetDict(drifted_datasets_dict)

    if isinstance(dataset, DatasetDict):
        return drift_dataset_dict(dataset, drift_ratios)
    else:
        return drift_dataset(dataset, drift_ratios)


class MemoryToInsert(TypedDict):
    text: str | None
    image: bytes | Image.Image | None
    label: int
    label_name: str | None
    metadata: str | None
    memory_version: int
    embedding: np.ndarray | None


def _transform_to_memory_to_insert_dict(
    item: LabeledMemory | Mapping | tuple, mode: Literal["hosted", "local"] = "local"
) -> MemoryToInsert:
    match item:
        case LabeledMemory():
            memory_to_insert: MemoryToInsert = {
                "text": item.value if isinstance(item.value, str) else None,
                "image": (
                    pil_image_to_bytes(item.value)
                    if mode == "local" and isinstance(item.value, Image.Image)
                    else item.value
                    if isinstance(item.value, Image.Image)
                    else None
                ),
                "label": item.label,
                "label_name": item.label_name,
                "metadata": json.dumps(item.metadata) if item.metadata else None,
                "memory_version": 1,
                "embedding": None,
            }
            return memory_to_insert
        # This also handles the dict case
        case Mapping():
            if "value" in item and "label" in item:
                value = item["value"]
                label = item["label"]
                label_name = item.get("label_name", None)
                metadata = item.get("metadata", None)
            elif "text" in item and "label" in item:
                value = item["text"]
                label = item["label"]
                label_name = item.get("label_name", None)
                metadata = item.get("metadata", None)
            elif "image" in item and "label" in item:
                value = item["image"]
                label = item["label"]
                label_name = item.get("label_name", None)
                metadata = item.get("metadata", None)
            elif "label" in item:
                keys = list(item.keys())

                label = item["label"]
                if label is None:
                    raise ValueError("Label must be provided.")
                keys.remove("label")

                label_name = item.get("label_name", None)
                if label_name:
                    keys.remove("label_name")

                metadata = item.get("metadata", None)
                if metadata:
                    keys.remove("metadata")

                if len(keys) == 1:
                    value = item[keys[0]]
                else:
                    raise ValueError("No 'value' column found and one could not be inferred.")
            else:
                raise ValueError("List of dicts does not contain 'value' and 'label' columns")

            ## Validate dictionary values ##

            # if value is bytes, transform to image before validation
            value = bytes_to_pil_image(value) if isinstance(value, bytes) else value

            # value validation
            if not isinstance(value, InputType):
                raise ValueError("value must be a string or PIL Image.")

            # Label validation
            if not isinstance(label, int):
                raise ValueError("Label must be an int.")

            # Label name validation
            if label_name is not None and not isinstance(label_name, str):
                raise ValueError("Label name must be a string.")

            # Metadata validation
            if metadata is not None:
                if not isinstance(metadata, (str, dict)):
                    raise ValueError("Metadata must be a JSON-serializable string or dict.")
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        raise ValueError("Metadata must be a JSON-serializable string or dict.")

            memory_to_insert: MemoryToInsert = {
                "text": value if isinstance(value, str) else None,
                "image": (
                    pil_image_to_bytes(value)
                    if mode == "local" and isinstance(value, Image.Image)
                    else value
                    if isinstance(value, Image.Image)
                    else None
                ),
                "label": label,
                "label_name": label_name,
                "metadata": json.dumps(metadata) if metadata else None,
                "memory_version": 1,
                "embedding": None,
            }
            return memory_to_insert

        case tuple():
            if len(item) == 2 and isinstance(item[0], InputType) and (isinstance(item[1], int)):
                memory_to_insert: MemoryToInsert = {
                    "text": item[0] if isinstance(item[0], str) else None,
                    "image": (
                        pil_image_to_bytes(item[0])
                        if mode == "local" and isinstance(item[0], Image.Image)
                        else item[0]
                        if isinstance(item[0], Image.Image)
                        else None
                    ),
                    "label": item[1],
                    "memory_version": 1,
                    "embedding": None,
                    "metadata": None,
                    "label_name": None,
                }
                return memory_to_insert
            else:
                raise ValueError(
                    "Tuple must only have two elements; the first being the data and the second being the label."
                )
        case _:
            raise ValueError(f"Item must be a LabeledMemory, a Mapping, or a tuple: {type(item)}")


def transform_data_to_dict_list(data: DatasetLike, mode: Literal["hosted", "local"] = "local") -> list[MemoryToInsert]:
    match data:
        case LabeledMemory():
            return [_transform_to_memory_to_insert_dict(data, mode)]
        case dict():
            return [_transform_to_memory_to_insert_dict(data, mode)]
        case list():
            return [_transform_to_memory_to_insert_dict(item, mode) for item in data]
        case pd.DataFrame():
            return [_transform_to_memory_to_insert_dict(item, mode) for item in data.to_dict("records")]
        case Dataset():
            return [_transform_to_memory_to_insert_dict(item, mode) for item in data]  # type: ignore -- For our purposes, we can assume the item type is a Mapping
        case TorchDataset():
            return [_transform_to_memory_to_insert_dict(item, mode) for item in data]
        case TorchDataLoader():
            return [_transform_to_memory_to_insert_dict(item[0], mode) for item in data]
        case _:
            raise ValueError(
                f"Dataset must be a list of tuples, dicts, or LabeledMemories, or a single DataFrame, HuggingFace Dataset, Torch Dataset, Torch Data Loader, LabeledMemory, or dict: {type(data)}"
            )


class MemoryRecord(TypedDict):
    id: str
    text: str | None
    image: bytes | None
    label: int
    label_name: str | None
    embedding: np.ndarray
    metadata: str | None


def transform_rows_to_labeled_memories(
    memory_records: list[dict[str, Any]] | list[tuple[int, dict[ColumnName, Any]]]
) -> list[LabeledMemory]:
    if isinstance(memory_records[0], tuple):
        memory_records = cast(list[tuple[int, dict[ColumnName, Any]]], memory_records)
        memory_records = [{"_rowid": memory_record[0], **memory_record[1]} for memory_record in memory_records]

    memoryset: list[LabeledMemory] = []
    for record in memory_records:
        memory_record = cast(MemoryRecord, record)
        label = memory_record.get("label", None)
        if label is None:
            raise ValueError("Label must be provided.")
        else:
            metadata = memory_record.get("metadata", None)
            memoryset.append(
                LabeledMemory(
                    value=memory_record.get("value", memory_record.get("text", memory_record.get("image", None))),
                    label=label,
                    label_name=memory_record.get("label_name", None),
                    embedding=memory_record.get("embedding"),
                    metadata=json.loads(metadata) if metadata else None,
                    memory_version=memory_record.get("memory_version", 1),
                    memory_id=cast(int, memory_record.get("_rowid")),
                )
            )
    return memoryset


###### Memoryset Lookup Utils ######


class MemoryLookupResults(TypedDict):
    """Column-oriented LabeledMemoryset lookup query results."""

    value: list[InputType]
    label: list[int]
    label_name: list[str | None]
    embedding: list[np.ndarray]
    metadata: list[dict[str, Any] | None]
    lookup_score: list[float]
    memory_id: list[int]
    memory_version: list[int]


def format_lookup_results(
    results: tuple[int, list], original_query: np.ndarray, column_oriented: bool | None = False
) -> MemoryLookupResults | list[LabeledMemoryLookup]:
    if column_oriented:
        formatted_results: MemoryLookupResults | list[LabeledMemoryLookup] = {
            "value": [],
            "embedding": [],
            "memory_id": [],
            "memory_version": [],
            "label": [],
            "label_name": [],
            "metadata": [],
            "lookup_score": [],
        }
    else:
        formatted_results: MemoryLookupResults | list[LabeledMemoryLookup] = []

    for row in results[1]:
        metadata = json.loads(row[0]) if row[0] is not None else None
        if row[1] is not None:
            if isinstance(row[1], bytes):
                value = bytes_to_pil_image(row[1])
            else:
                value = row[1]
        else:
            value = row[2]

        if column_oriented:
            assert isinstance(formatted_results, dict)
            formatted_results["value"].append(value)
            formatted_results["embedding"].append(np.array(row[6]))
            formatted_results["memory_id"].append(row[7])
            formatted_results["memory_version"].append(row[5])
            formatted_results["label"].append(row[3])
            formatted_results["label_name"].append(row[4])
            formatted_results["metadata"].append(metadata)
            formatted_results["lookup_score"].append(np.dot(original_query, np.array(row[6])))
        else:
            assert isinstance(formatted_results, list)
            formatted_results.append(
                LabeledMemoryLookup(
                    value=value,
                    embedding=row[6],  # embedding
                    memory_id=row[7],  # row_id for the memory data accessed
                    memory_version=row[5],  # memory_version
                    label=row[3],  # label
                    label_name=row[4],  # label_name
                    metadata=metadata,
                    lookup_score=np.dot(original_query, np.array(row[6])),  # Calculate inner product
                )
            )
    return formatted_results
