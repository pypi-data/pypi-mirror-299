from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest
import torch
from datasets import ClassLabel, Dataset, Features, Value
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset

from orcalib.rac.common import (
    InputType,
    LabeledMemoryLookup,
    LabeledMemoryLookupResult,
    PredictionResult,
)
from orcalib.rac.memoryset import LabeledMemoryset
from orcalib.rac.rac import EvalResult, RACModel

test_rac = RACModel(num_classes=3)
# fake predictions because predict_batch is not implemented
predictions: list[PredictionResult] = [
    PredictionResult(
        label=0,
        confidence=0.9,
        memories=[
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                attention_weight=0.9,
                memory_version=0,
                memory_id=1,
                embedding=np.random.rand(768).tolist(),
            ),
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                attention_weight=0.9,
                memory_version=0,
                memory_id=2,
                embedding=np.random.rand(768).tolist(),
            ),
        ],
        feedback=lambda x, y: 1.0,
        logits=torch.tensor([0.0, 0.9, 0.1]),
    ),
    PredictionResult(
        label=0,
        confidence=0.9,
        memories=[
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=1,
                embedding=np.random.rand(768).tolist(),
            ),
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=2,
                embedding=np.random.rand(768).tolist(),
            ),
        ],
        feedback=lambda x, y: 1.0,
        logits=torch.tensor([0.0, 0.1, 0.9]),
    ),
    PredictionResult(
        label=1,
        confidence=0.9,
        memories=[
            LabeledMemoryLookup(
                value="bear",
                label=1,
                label_name="bear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=1,
                embedding=np.random.rand(768).tolist(),
            ),
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=2,
                embedding=np.random.rand(768).tolist(),
            ),
        ],
        feedback=lambda x, y: 1.0,
        logits=torch.tensor([0.9000, 0.0000, 0.1000]),
    ),
    PredictionResult(
        label=1,
        confidence=0.9,
        memories=[
            LabeledMemoryLookup(
                value="bear",
                label=1,
                label_name="bear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=1,
                embedding=np.random.rand(768).tolist(),
            ),
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=2,
                embedding=np.random.rand(768).tolist(),
            ),
        ],
        feedback=lambda x, y: 1.0,
        logits=torch.tensor([0.9000, 0.0000, 0.1000]),
    ),
    PredictionResult(
        label=1,
        confidence=0.9,
        memories=[
            LabeledMemoryLookup(
                value="bear",
                label=1,
                label_name="bear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=1,
                embedding=np.random.rand(768).tolist(),
            ),
            LabeledMemoryLookup(
                value="pear",
                label=0,
                label_name="pear",
                lookup_score=0.5,
                memory_version=0,
                attention_weight=0.9,
                memory_id=2,
                embedding=np.random.rand(768).tolist(),
            ),
        ],
        feedback=lambda x, y: 1.0,
        logits=torch.tensor([0.9000, 0.0000, 0.1000]),
    ),
]

test_rac.predict_batch = MagicMock(return_value=predictions)

# Sample data
data_dict = {
    "value": ["test", "bread", "air", "bread", "test"],
    "label": [0, 1, 2, 1, 0],
}

tuple_dataset: list[tuple[InputType, int]] = [
    ("test", 0),
    ("bread", 1),
    ("air", 2),
    ("bread", 1),
    ("test", 0),
]

expected_stats = EvalResult(
    accuracy=0.4,
    f1=0.3,
    roc_auc=0.4305555555555555,
    loss=1.2983691692352295,
)


def test_eval_accepts_memoryset():
    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    # "value": ["test", "bread", "air", "bread", "test"],
    # "label": [0, 1, 2, 1, 0],
    memoryset.insert(
        [
            {
                "value": "test",
                "label": 0,
            },
            {
                "value": "bread",
                "label": 1,
            },
            {
                "value": "air",
                "label": 2,
            },
            {
                "value": "bread",
                "label": 1,
            },
            {
                "value": "test",
                "label": 0,
            },
        ]
    )
    stats = test_rac.evaluate(memoryset)
    assert stats == expected_stats

    stats_explain = test_rac.evaluate_and_explain(tuple_dataset)
    assert stats_explain == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )

    # drop the data
    memoryset.drop_all_data(yes_i_am_sure=True)


def test_eval_accepts_tuple():
    stats = test_rac.evaluate(tuple_dataset)
    assert stats == expected_stats

    stats_explain = test_rac.evaluate_and_explain(tuple_dataset)
    assert stats_explain == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )


def test_eval_accepts_dataframe():
    dataframe = pd.DataFrame(
        [
            {"value": "test", "label": 0},
            {"value": "bread", "label": 1},
            {"value": "air", "label": 2},
            {"value": "bread", "label": 1},
            {"value": "test", "label": 0},
        ]
    )

    stats = test_rac.evaluate(dataset=dataframe)

    assert stats == expected_stats
    stats_explain = test_rac.evaluate_and_explain(dataset=dataframe)

    assert stats_explain == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )


def test_eval_accepts_HF_dataset():
    # Define the features
    features = Features(
        {
            "value": Value(dtype="string"),
            "label": ClassLabel(names=["test", "bread", "air"]),
        }
    )

    # Create the dataset
    hf_dataset = Dataset.from_dict(data_dict, features=features)

    assert test_rac.evaluate(dataset=hf_dataset) == expected_stats
    assert test_rac.evaluate_and_explain(dataset=hf_dataset) == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )


def test_eval_accepts_pytorch_dataset_and_dataloader():
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
    stats_dataloader = test_rac.evaluate(dataset=torch_dataloader)
    stats_dataset = test_rac.evaluate(dataset=torch_dataset)
    stats_dataloader_explain = test_rac.evaluate_and_explain(dataset=torch_dataloader)
    stats_dataset_explain = test_rac.evaluate_and_explain(dataset=torch_dataset)

    assert stats_dataloader == expected_stats

    assert stats_dataset == expected_stats
    assert stats_dataloader_explain == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )

    assert stats_dataset_explain == (
        expected_stats,
        {
            1: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
            2: LabeledMemoryLookupResult(correct=2, incorrect=3, label=0, ratio=0.4, total=5),
        },
    )


def test_eval_raises_when_given_invalid_input():
    with pytest.raises(TypeError):
        (test_rac.evaluate(dataset="this is not a valid dataset"))  # type: ignore
