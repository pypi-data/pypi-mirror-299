import hashlib
from unittest.mock import patch

import pytest

from orcalib.rac.embedding_models import EmbeddingModel
from orcalib.rac.memoryset import LabeledMemoryset, _get_embedding_hash

# Test table and database name init


def test_local_passed_table_name():
    M = LabeledMemoryset("file:./delete_me_test_db#test_table")
    assert M.table_name == "test_table"

    # drop the data
    M.drop_all_data(yes_i_am_sure=True)


def test_local_default_table_name():
    M = LabeledMemoryset("file:./delete_me_test_db")
    assert M.table_name == "memories"

    # drop the data
    M.drop_all_data(yes_i_am_sure=True)


def test_local_bad_fragment():
    with pytest.raises(ValueError, match=r"^Table name*"):
        LabeledMemoryset("file:./delete_me_test_db#table_name=bad_table")


def test_local_bad_table_name():
    with pytest.raises(ValueError, match=r"^Table name*"):
        LabeledMemoryset("file:./delete_me_test_db#123table")


@patch("orcalib.rac.memoryset.OrcaDatabase")
def test_hosted_passed_db_and_table_name(mock_orca):
    M = LabeledMemoryset(
        uri="http://localhost:1583/database_name#test_table",
        secret_key="my_secret_key",
        api_key="my_api_key",
    )
    assert M.table_name == "test_table"
    assert M.database_name == "database_name"


@patch("orcalib.rac.memoryset.OrcaDatabase")
def test_hosted_default_db_and_table_name(mock_orca):
    M = LabeledMemoryset(
        uri="http://localhost:1583/",
        secret_key="my_secret_key",
        api_key="my_api_key",
    )
    assert M.table_name == "memories"
    assert M.database_name == "default"


def test_hosted_bad_table_name():
    with pytest.raises(ValueError, match=r"^Table name*"):
        LabeledMemoryset(
            uri="http://localhost:1583/#table_name=bad_table",
            secret_key="my_secret_key",
            api_key="my_api_key",
        )


def test_hosted_too_many_paths():
    with pytest.raises(ValueError, match=r"^Database name*"):
        LabeledMemoryset(
            uri="http://localhost:1583/database/name",
            secret_key="my_secret_key",
            api_key="my_api_key",
        )


def test_hosted_bad_database_name():
    with pytest.raises(ValueError, match=r"^Database name*"):
        LabeledMemoryset(
            uri="http://localhost:1583/database%^&",
            secret_key="my_secret_key",
            api_key="my_api_key",
        )


def test_get_embedding_hash():
    sample_array = EmbeddingModel.CLIP_BASE._get_embedding("Test a real embedding")[0]
    expected_hash = hashlib.sha256(sample_array.tobytes()).hexdigest()

    result_hash = _get_embedding_hash(sample_array)

    assert result_hash == expected_hash, f"Expected {expected_hash}, but got {result_hash}"


def test_get_embedding_hash_always_returns_same():
    sample_array = EmbeddingModel.CLIP_BASE._get_embedding("Test a real embedding")[0]

    result_hash1 = _get_embedding_hash(sample_array)
    result_hash2 = _get_embedding_hash(sample_array)

    assert result_hash1 == result_hash2
