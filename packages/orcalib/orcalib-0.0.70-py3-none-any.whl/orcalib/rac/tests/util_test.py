import json
from collections import Counter
from typing import Any, cast

import numpy as np
import pandas as pd
import pytest
from datasets import ClassLabel, Dataset, DatasetDict, Features, Value
from PIL import Image
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset

from orcalib.rac.common import InputType, LabeledMemory
from orcalib.rac.util import (
    MemoryToInsert,
    drift_classes,
    format_dataset,
    pil_image_to_bytes,
    transform_data_to_dict_list,
)

#################### Formatting Dataset Tests ####################

# Sample data
data_dict = {
    "value": ["test", "bread", "air", "bread", "test"],
    "label": [0, 1, 2, 1, 0],
}

data_dict_image = {
    "image": ["test", "bread", "air", "bread", "test"],
    "label": [0, 1, 2, 1, 0],
}

data_dict_text = {
    "text": ["test", "bread", "air", "bread", "test"],
    "label": [0, 1, 2, 1, 0],
}

tuple_dataset: list[tuple[InputType, int]] = [
    ("test", 0),
    ("bread", 1),
    ("air", 2),
    ("bread", 1),
    ("test", 0),
]


def test_format_dataset_accepts_tuple():
    formatted_dataset = format_dataset(tuple_dataset)
    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_dataframe():
    data = [
        {"value": "test", "label": 0},
        {"value": "bread", "label": 1},
        {"value": "air", "label": 2},
        {"value": "bread", "label": 1},
        {"value": "test", "label": 0},
    ]

    dataframe = pd.DataFrame(data)

    formatted_dataset = format_dataset(dataset=dataframe)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_dataframe_with_image_key():
    data = [
        {"image": "test", "label": 0},
        {"image": "bread", "label": 1},
        {"image": "air", "label": 2},
        {"image": "bread", "label": 1},
        {"image": "test", "label": 0},
    ]

    dataframe = pd.DataFrame(data)

    formatted_dataset = format_dataset(dataset=dataframe)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_dataframe_with_text_key():
    data = [
        {"text": "test", "label": 0},
        {"text": "bread", "label": 1},
        {"text": "air", "label": 2},
        {"text": "bread", "label": 1},
        {"text": "test", "label": 0},
    ]

    dataframe = pd.DataFrame(data)

    formatted_dataset = format_dataset(dataset=dataframe)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_partially_labeled_pandas_dataframe():
    data = [
        {"input": "test", "label": 0},
        {"input": "bread", "label": 1},
        {"input": "air", "label": 2},
        {"input": "bread", "label": 1},
        {"input": "test", "label": 0},
    ]

    dataframe = pd.DataFrame(data)

    formatted_dataset = format_dataset(dataset=dataframe)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_partially_labeled_HF_dataset():
    # Define the features
    features = Features(
        {
            "input": Value(dtype="string"),
            "label": ClassLabel(names=["test", "bread", "air"]),
        }
    )

    one_label_data_dict = {
        "input": ["test", "bread", "air", "bread", "test"],
        "label": [0, 1, 2, 1, 0],
    }
    # Create the dataset
    hf_dataset = Dataset.from_dict(one_label_data_dict, features=features)

    formatted_dataset = format_dataset(dataset=hf_dataset)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_HF_dataset():
    # Define the features
    features = Features(
        {
            "value": Value(dtype="string"),
            "label": ClassLabel(names=["test", "bread", "air"]),
        }
    )

    # Create the dataset
    hf_dataset = Dataset.from_dict(data_dict, features=features)

    formatted_dataset = format_dataset(dataset=hf_dataset)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_HF_dataset_with_image_key():
    # Define the features
    features = Features(
        {
            "image": Value(dtype="string"),
            "label": ClassLabel(names=["test", "bread", "air"]),
        }
    )
    hf_dataset = Dataset.from_dict(data_dict_image, features=features)

    formatted_dataset = format_dataset(dataset=hf_dataset)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_HF_dataset_with_text_key():
    # Define the features
    features = Features(
        {
            "text": Value(dtype="string"),
            "label": ClassLabel(names=["test", "bread", "air"]),
        }
    )
    hf_dataset = Dataset.from_dict(data_dict_text, features=features)

    formatted_dataset = format_dataset(dataset=hf_dataset)

    assert formatted_dataset == tuple_dataset


def test_format_dataset_accepts_pytorch_dataset_and_dataloader():
    class TorchDatasetSubclassed(TorchDataset):
        def __init__(self, value, label):
            self.value = value
            self.label = label

        def __getitem__(self, idx):
            return {"value": self.value[idx], "label": self.label[idx]}

        def __len__(self):
            return len(self.value)

    torch_dataset = TorchDatasetSubclassed(value=data_dict["value"], label=data_dict["label"])

    torch_dataloader = TorchDataLoader(torch_dataset, batch_size=1)
    formatted_dataloader = format_dataset(dataset=torch_dataloader)
    formatted_torch_dataset = format_dataset(dataset=torch_dataset)

    assert formatted_dataloader == tuple_dataset
    assert formatted_torch_dataset == tuple_dataset


def test_format_dataset_accepts_partially_labeled_pytorch_dataset_and_dataloader():
    class TorchDatasetSubclassed(TorchDataset):
        def __init__(self, input, label):
            self.input = input
            self.label = label

        def __getitem__(self, idx):
            return {"input": self.input[idx], "label": self.label[idx]}

        def __len__(self):
            return len(self.input)

    torch_dataset = TorchDatasetSubclassed(input=data_dict["value"], label=data_dict["label"])

    torch_dataloader = TorchDataLoader(torch_dataset, batch_size=1)
    formatted_torch_dataloader = format_dataset(dataset=torch_dataloader)
    formatted_torch_dataset = format_dataset(dataset=torch_dataset)

    assert formatted_torch_dataloader == tuple_dataset
    assert formatted_torch_dataset == tuple_dataset


def test_format_dataset_raises_when_given_tuple_with_greater_than_2_columns():
    bad_tuple_dataset = [
        ("test", 0, "extra"),
        ("bread", 1, "extra"),
        ("air", 2, "extra"),
        ("bread", 1, "extra"),
        ("test", 0, "extra"),
    ]

    with pytest.raises(TypeError):
        format_dataset(bad_tuple_dataset)  # type: ignore


def test_format_dataset_accepts_dict():
    data = [
        {"value": "test", "label": 0},
        {"value": "bread", "label": 1},
        {"value": "air", "label": 2},
        {"value": "bread", "label": 1},
        {"value": "test", "label": 0},
    ]

    formatted_dataset = format_dataset(dataset=data)

    assert [formatted_dataset[0]] == format_dataset(dataset=data[0])
    assert formatted_dataset == format_dataset(dataset=data)


def test_format_dataset_accepts_dict_with_image_key():
    data = [
        {"image": "test", "label": 0},
        {"image": "bread", "label": 1},
        {"image": "air", "label": 2},
        {"image": "bread", "label": 1},
        {"image": "test", "label": 0},
    ]

    formatted_dataset = format_dataset(dataset=data)

    assert [formatted_dataset[0]] == format_dataset(dataset=data[0])
    assert formatted_dataset == format_dataset(dataset=data)


def test_format_dataset_accepts_dict_with_text_key():
    data = [
        {"text": "test", "label": 0},
        {"text": "bread", "label": 1},
        {"text": "air", "label": 2},
        {"text": "bread", "label": 1},
        {"text": "test", "label": 0},
    ]

    formatted_dataset = format_dataset(dataset=data)

    assert [formatted_dataset[0]] == format_dataset(dataset=data[0])
    assert formatted_dataset == format_dataset(dataset=data)


#################### Transforming to and from LabeledMemorys ####################


def test_transform_data_to_dict_list_from_labeled_memories():
    # Test case 1: LabeledMemory input
    memory: MemoryToInsert = {
        "text": "National Parks are fun",
        "image": None,
        "label": 1,
        "label_name": "Outdoor Recreation",
        "metadata": None,
        "memory_version": 1,
        "embedding": None,
    }
    assert transform_data_to_dict_list(
        LabeledMemory(
            value="National Parks are fun",
            label=1,
            label_name="Outdoor Recreation",
            metadata=None,
            memory_version=0,
            memory_id=1,
            embedding=np.random.rand(768).tolist(),
        )
    ) == [memory]

    # Test case 2: list of LabeledMemory input
    memories = [
        LabeledMemory(
            value="National Parks are fun",
            label=1,
            label_name="Outdoor Recreation",
            metadata=None,
            memory_version=0,
            memory_id=1,
            embedding=np.random.rand(768).tolist(),
        ),
        LabeledMemory(
            value=Image.open("./orcalib/rac/tests/test_image.png"),
            label=1,
            label_name="Outdoor Recreation",
            metadata=None,
            memory_version=0,
            memory_id=1,
            embedding=np.random.rand(768).tolist(),
        ),
    ]
    memories_to_insert: list[MemoryToInsert] = [
        memory,
        {
            "text": None,
            "image": pil_image_to_bytes(Image.open("./orcalib/rac/tests/test_image.png")),
            "label": 1,
            "label_name": "Outdoor Recreation",
            "metadata": None,
            "memory_version": 1,
            "embedding": None,
        },
    ]
    assert transform_data_to_dict_list(memories) == memories_to_insert


inputs = [
    {
        "value": "value1",
        "label": 1,
        "label_name": "label_name1",
        "metadata": {"value_metadata": "metadata1"},
    },
    {
        "value": "value2",
        "label": 2,
        "label_name": "label_name2",
        "metadata": {"value_metadata": "metadata2"},
    },
]

expected_memories_to_insert: list[MemoryToInsert] = [
    {
        "text": "value1",
        "image": None,
        "label": 1,
        "label_name": "label_name1",
        "metadata": json.dumps({"value_metadata": "metadata1"}),
        "memory_version": 1,
        "embedding": None,
    },
    {
        "text": "value2",
        "image": None,
        "label": 2,
        "label_name": "label_name2",
        "metadata": json.dumps({"value_metadata": "metadata2"}),
        "memory_version": 1,
        "embedding": None,
    },
]

expected_simple_memory_to_insert: MemoryToInsert = {
    "text": "this is text",
    "image": None,
    "label": 3,
    "label_name": None,
    "metadata": None,
    "memory_version": 1,
    "embedding": None,
}

expected_simple_memory_to_insert_with_label_name: MemoryToInsert = {
    "text": None,
    "image": pil_image_to_bytes(Image.open("./orcalib/rac/tests/test_image.png")),
    "label": 3,
    "label_name": "label_name",
    "metadata": None,
    "memory_version": 1,
    "embedding": None,
}


@pytest.mark.parametrize(
    "input, expected_memories",
    [
        (inputs[0], [expected_memories_to_insert[0]]),
        (inputs, expected_memories_to_insert),
        (
            [{"label": 3, "text": "this is text"}],
            [expected_simple_memory_to_insert],
        ),
        (
            [{"label": 3, "image": Image.open("./orcalib/rac/tests/test_image.png"), "label_name": "label_name"}],
            [expected_simple_memory_to_insert_with_label_name],
        ),
    ],
)
def test_transform_data_to_dict_list_from_dict(
    input: dict | list[dict], expected_memories: LabeledMemory | list[LabeledMemory]
):
    assert transform_data_to_dict_list(input) == expected_memories


@pytest.mark.parametrize(
    "input",
    [
        [{"label": 3}],
        {"label": 3, "not_correct_value_key": "this is text", "something_else": "this is ignored"},
        {"value": 12, "label": 1},
        {"value": "test", "label": "string"},
        {"text": "test", "label": ("string")},
        {"value": "test", "label": 1, "label_name": 2},
        {"text": "test", "label": 1, "label_name": "test", "metadata": 2},
        {"value": "test", "label": 1, "label_name": "test", "metadata": "string"},
    ],
)
def test_transform_data_to_dict_list_errors(input: dict | list[dict]):
    with pytest.raises(ValueError):
        transform_data_to_dict_list(input)


def test_transform_data_to_dict_list_from_tuple():
    # list of tuples input
    data: list[tuple[InputType, int]] = [
        (
            cast(InputType, "value1"),
            1,
        )
    ]
    expected_memory_to_insert: MemoryToInsert = {
        "text": "value1",
        "image": None,
        "label": 1,
        "label_name": None,
        "metadata": None,
        "memory_version": 1,
        "embedding": None,
    }
    assert transform_data_to_dict_list(data) == [expected_memory_to_insert]


def test_transform_data_to_dict_list_from_tuple_error():
    # list of tuples input
    data = [(cast(InputType, "value1"), 1, "something else")]

    with pytest.raises(ValueError):
        transform_data_to_dict_list(data)  # type: ignore -- testing bad type


def test_transform_data_to_dict_list_from_dataframe():
    # pd.DataFrame input
    data = pd.DataFrame(
        [
            {
                "value": "value1",
                "label": 1,
                "label_name": "label_name1",
                "metadata": {"value_metadata": "metadata1"},
            },
            {
                "value": "value2",
                "label": 2,
                "label_name": "label_name2",
                "metadata": {"value_metadata": "metadata2"},
            },
        ]
    )
    assert transform_data_to_dict_list(data) == expected_memories_to_insert


def test_transform_data_to_dict_list_from_hf_dataset():
    # HuggingFace Dataset input

    data = Dataset.from_dict(
        {
            "value": ["Sea turtles are really cool"],
            "label": [0],
            "label_name": ["sea animals"],
            "metadata": [{"value_metadata": "metadata"}],
            "memory_version": [1],
        }
    )
    expected_memory_to_insert: MemoryToInsert = {
        "text": "Sea turtles are really cool",
        "image": None,
        "label": 0,
        "label_name": "sea animals",
        "metadata": json.dumps({"value_metadata": "metadata"}),
        "memory_version": 1,
        "embedding": None,
    }

    assert transform_data_to_dict_list(data) == [expected_memory_to_insert]


def test_transform_data_to_dict_list_from_torch_dataset():
    #  TorchDataset and TorchDataLoader input

    class TorchDatasetSubclassed(TorchDataset):
        def __init__(
            self,
            value: list[InputType],
            label: list[int],
            label_name: list[str | None],
            metadata: list[dict[str, Any] | None],
            memory_version: list[int],
        ):
            self.value = value
            self.label = label
            self.label_name = label_name
            self.metadata = metadata
            self.memory_version = memory_version

        def __getitem__(self, idx):
            return {
                "value": self.value[idx],
                "label": self.label[idx],
                "label_name": self.label_name[idx],
                "metadata": self.metadata[idx],
                "memory_version": self.memory_version[idx],
            }

        def __len__(self):
            return len(self.value)

    torch_dataset = TorchDatasetSubclassed(
        value=data_dict["value"],
        label=data_dict["label"],
        label_name=[None, "None", None, None, None],
        metadata=[None, {"foo": "bar"}, None, None, None],
        memory_version=[1, 1, 1, 1, 1],
    )

    def collate(item):
        if item is None:
            return item
        return item

    torch_dataloader = TorchDataLoader(torch_dataset, batch_size=1, collate_fn=collate)

    memories: list[MemoryToInsert] = [
        {
            "text": "test",
            "image": None,
            "embedding": None,
            "label": 0,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
        },
        {
            "text": "bread",
            "image": None,
            "embedding": None,
            "label": 1,
            "label_name": "None",
            "metadata": json.dumps({"foo": "bar"}),
            "memory_version": 1,
        },
        {
            "text": "air",
            "image": None,
            "embedding": None,
            "label": 2,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
        },
        {
            "text": "bread",
            "image": None,
            "embedding": None,
            "label": 1,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
        },
        {
            "text": "test",
            "image": None,
            "embedding": None,
            "label": 0,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
        },
    ]
    assert transform_data_to_dict_list(torch_dataset) == memories
    assert transform_data_to_dict_list(torch_dataloader) == memories


def test_drift_classes_from_dataset_dict():
    #  Create a balanced dataset dict with one feature, 2 classes, and 100 rows
    train = {"train": []}
    for label in range(2):
        for j in range(50):
            train["train"].append(
                {
                    "value": f"value_{j}",
                    "label": label,
                }
            )
    input_dataset_dict: DatasetDict = DatasetDict({"train": Dataset.from_dict(train)["train"]})

    balanced_label_counts = Counter(item["label"] for item in input_dataset_dict["train"])  # type: ignore
    assert balanced_label_counts[0] == 50

    #  Drift the dataset to have 10% of class 0
    new_dataset_dict = drift_classes(input_dataset_dict, {0: 0.1})
    imbalanced_label_counts = Counter(item["label"] for item in new_dataset_dict["train"])  # type: ignore
    assert imbalanced_label_counts[0] == 5
    assert imbalanced_label_counts[1] == 50


def test_drift_classes_from_dataset():
    #  Create a balanced dataset with 2 classes and 100 rows
    train = []
    for label in range(2):
        for j in range(50):
            train.append(
                {
                    "value": f"value_{j}",
                    "label": label,
                }
            )
    input_dataset = Dataset.from_list(train)
    balanced_label_counts = Counter(item["label"] for item in input_dataset)  # type: ignore
    assert balanced_label_counts[0] == 50

    #  Drift the dataset to have 10% of class 0
    new_dataset = drift_classes(input_dataset, {0: 0.1})
    imbalanced_label_counts = Counter(item["label"] for item in new_dataset)  # type: ignore
    assert imbalanced_label_counts[0] == 5
    assert imbalanced_label_counts[1] == 50
