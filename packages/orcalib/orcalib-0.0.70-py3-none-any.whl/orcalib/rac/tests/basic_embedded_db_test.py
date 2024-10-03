from unittest.mock import patch

import lancedb
import numpy as np
import pandas as pd
import pytest
from numpy.linalg import norm
from PIL import Image, ImageChops

from orcalib.rac.common import LabeledMemory
from orcalib.rac.embedding_models import EmbeddingModel
from orcalib.rac.memoryset import LabeledMemoryset, _get_embedding_hash


def images_are_approximately_equal(image1: Image.Image, image2: Image.Image, tolerance: float = 0.1) -> bool:
    # Ensure both images are in the same mode and size
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")

    if image1.size != image2.size:
        image2 = image2.resize(image1.size)

    # Compute the difference between the two images
    diff = ImageChops.difference(image1, image2)

    # Convert the difference image to a numpy array
    diff_array = np.array(diff)

    # Calculate the total difference
    total_diff = np.sum(np.abs(diff_array))

    # Normalize by the number of pixels and color channels
    max_diff = np.prod(diff_array.shape) * 255  # 255 is the maximum possible difference per channel
    normalized_diff = total_diff / max_diff

    # Check if the normalized difference is within the tolerance
    return normalized_diff <= tolerance


def test_insert_and_lookup_multimodal():
    test_image = Image.open("./orcalib/rac/tests/test_image.png")
    test_text = "Scooby Doo where are you?"

    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    memoryset.insert(
        [
            {
                "value": test_image,
                "label": 7,
                "label_name": "Biters",
                "metadata": {"source": "screenshot"},
            },
            {
                "value": test_text,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )
    # ensure the data is inserted
    assert len(memoryset) == 2

    # do a lookup (single and batch), ensure the correct top result is returned
    result1 = memoryset.lookup(memoryset.model._get_embedding("Some Cartoon Dog Thing"), k=1)
    assert len(result1) == 1
    assert isinstance(result1[0], list)
    assert result1[0][0].label == 1
    assert result1[0][0].value == "Scooby Doo where are you?"

    result1 = memoryset.lookup(memoryset.model._get_embedding("Some Cartoon Dog Thing")[0], k=1)
    assert len(result1) == 1
    assert isinstance(result1[0], list)
    assert result1[0][0].label == 1
    assert result1[0][0].value == "Scooby Doo where are you?"

    result2 = memoryset.lookup(memoryset.model._get_embedding(test_image), k=1)
    assert isinstance(result2[0], list)
    assert result2[0][0].label == 7
    assert images_are_approximately_equal(result2[0][0].value, test_image)  # type: ignore -- we know value is an image
    assert result2[0][0].metadata == {"source": "screenshot"}

    # drop the data
    memoryset.drop_all_data(yes_i_am_sure=True)


def test_lookup_column_oriented():
    test_image = Image.open("./orcalib/rac/tests/test_image.png")
    test_text = "Scooby Doo where are you?"

    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    memoryset.insert(
        [
            {
                "image": test_image,
                "label": 7,
                "label_name": "Biters",
                "metadata": {"source": "screenshot"},
            },
            {
                "text": test_text,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )
    # ensure the data is inserted
    assert len(memoryset) == 2

    # do a lookup (single and batch), ensure the correct top result is returned
    result = memoryset.lookup("Some Cartoon Dog Thing", k=1, column_oriented=True)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert result[0]["label"][0] == 1
    assert result[0]["value"][0] == "Scooby Doo where are you?"

    # drop the data
    memoryset.drop_all_data(yes_i_am_sure=True)


def test_clone_local_to_local():
    source = LabeledMemoryset("file:./delete_me_test_db_source")
    destination = LabeledMemoryset("file:./delete_me_test_db_destination")

    source.insert(
        {
            "value": "Scooby Doo where are you?",
            "label": 1,
            "label_name": "Scoooby!!",
            "metadata": {"source": "hanna babera"},
        }
    )

    destination.clone(source)

    result = destination.lookup(destination.model._get_embedding("Some Cartoon Dog Thing"), k=1)

    assert isinstance(result[0], list)
    assert result[0][0].label == 1
    assert result[0][0].value == "Scooby Doo where are you?"
    assert result[0][0].metadata == {"source": "hanna babera"}

    source.drop_all_data(yes_i_am_sure=True)
    destination.drop_all_data(yes_i_am_sure=True)


def test_map_local_to_local():
    source = LabeledMemoryset("file:./delete_me_test_db_source")
    destination = LabeledMemoryset("file:./delete_me_test_db_destination")

    source.insert(
        [
            {
                "value": "Scooby Doo where are you?",
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            }
        ]
    )

    def set_label(memory: LabeledMemory):
        if isinstance(memory.label, int):
            memory.label = memory.label + 1
        elif isinstance(memory.label, list):
            memory.label = [x + 1 for x in memory.label]  # type: ignore -- we know label is a list[int]
        return memory

    source.map(set_label, destination)

    result = destination.lookup(destination.model._get_embedding("Some Cartoon Dog Thing"), k=1)

    assert isinstance(result[0], list)
    assert result[0][0].label == 2
    assert result[0][0].value == "Scooby Doo where are you?"
    assert result[0][0].metadata == {"source": "hanna babera"}

    source.drop_all_data(yes_i_am_sure=True)
    destination.drop_all_data(yes_i_am_sure=True)


def _cos_sim(memory_embedding: np.ndarray, model_embedding: np.ndarray):
    return np.dot(memory_embedding, model_embedding) / (norm(memory_embedding) * norm(model_embedding))


def test_update_embedding_model_in_place():
    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    # Insert some data
    memoryset.insert(
        [
            {
                "value": "Scooby Doo where are you?",
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            }
        ]
    )
    assert memoryset.model == EmbeddingModel.CLIP_BASE

    memory = memoryset.lookup("Some Cartoon Dog Thing", k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.CLIP_BASE._get_embedding("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    # Update the embedding model
    new_model = EmbeddingModel.GTE_BASE
    memoryset.update_embedding_model(new_model)
    assert memoryset.model == new_model

    memory = memoryset.lookup("Some Cartoon Dog Thing", k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.GTE_BASE._get_embedding("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    memoryset.drop_all_data(yes_i_am_sure=True)


def test_update_embedding_model_new_destination():
    memoryset1 = LabeledMemoryset("file:./delete_me_test_db")

    # Insert some data
    memoryset1.insert(
        [
            {
                "value": "Scooby Doo where are you?",
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            }
        ]
    )
    assert memoryset1.model == EmbeddingModel.CLIP_BASE

    memory = memoryset1.lookup("Some Cartoon Dog Thing", k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.CLIP_BASE._get_embedding("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    # Update the embedding model
    new_model = EmbeddingModel.GTE_BASE
    memoryset2 = LabeledMemoryset("file:./delete_me_test_db_destination")
    memoryset1.update_embedding_model(new_model, memoryset2)
    assert memoryset2.model == new_model

    memory = memoryset2.lookup("Some Cartoon Dog Thing", k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.GTE_BASE._get_embedding("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    memoryset1.drop_all_data(yes_i_am_sure=True)
    memoryset2.drop_all_data(yes_i_am_sure=True)


def test_lookup_caching():
    test_text = "Scooby Doo where are you?"

    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    memoryset.insert(
        [
            {
                "value": test_text,
                "memory_version": 0,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )

    memory_embedding = memoryset.model._get_embedding("Some Cartoon Dog Thing")[0]
    # cache is empty initially
    assert memoryset.cache.currsize == 0

    assert isinstance(memoryset.db, lancedb.DBConnection)
    with patch.object(memoryset.db, "open_table", wraps=memoryset.db.open_table) as wrapped_open_table:
        result = memoryset.lookup(memoryset.model._get_embedding("Some Cartoon Dog Thing"), k=1)
        wrapped_open_table.assert_called_once()
        assert memoryset.cache[(_get_embedding_hash(memory_embedding), 1)] is not None
        assert len(memoryset.cache[(_get_embedding_hash(memory_embedding), 1)]) == len(result[0])

        memoryset.lookup(memoryset.model._get_embedding("Some Cartoon Dog Thing"), k=1)
        wrapped_open_table.assert_called_once()  # did not get called again

    memoryset.drop_all_data(yes_i_am_sure=True)


def test_metadata_mismatch():
    # default CLIP model
    memoryset = LabeledMemoryset("file:./delete_me_test_db")

    # try to re-initialize with a different model
    with pytest.raises(ValueError, match=r"^Model or model version mismatch*"):
        LabeledMemoryset("file:./delete_me_test_db", model=EmbeddingModel.GTE_BASE)

    memoryset.drop_all_data(yes_i_am_sure=True)


def test_existing_metadata():
    # default CLIP model
    memoryset = LabeledMemoryset("file:./delete_me_test_db")
    assert isinstance(memoryset.db, lancedb.DBConnection)
    assert memoryset.db.open_table(f"rac_meta_{memoryset.table_name}").count_rows() == 1

    # assert no error raised and row is not added
    memoryset_reconnect = LabeledMemoryset("file:./delete_me_test_db")
    assert isinstance(memoryset_reconnect.db, lancedb.DBConnection)
    assert memoryset_reconnect.db.open_table(f"rac_meta_{memoryset_reconnect.table_name}").count_rows() == 1

    memoryset.drop_all_data(yes_i_am_sure=True)
