# tests/test_query_utils.py

from unittest.mock import patch
from query_utils import get_sequence_query_results
from sg_connection import ShotGridConnector


@patch("query_utils.sg_connection")
def test_evaluate_query_fields_success(mock_sg):
    # Setup mock to return successful query result
    mock_sg.find_one.return_value = {
        "id": 123,
        "field1": "value1",
        "field2": 42
    }

    from query_utils import evaluate_query_fields
    result = evaluate_query_fields("Entity", 123, ["field1", "field2"])

    # Verify correct call to find_one
    mock_sg.find_one.assert_called_once_with(
        "Entity",
        [["id", "is", 123]],
        ["field1", "field2"]
    )

    # Verify returned values
    assert result == {"field1": "value1", "field2": 42}


@patch("query_utils.sg_connection")
def test_evaluate_query_fields_missing_fields(mock_sg):
    # Setup mock to return result with missing fields
    mock_sg.find_one.return_value = {
        "id": 123,
        "field1": "value1"
        # field2 is missing
    }

    from query_utils import evaluate_query_fields
    result = evaluate_query_fields("Entity", 123, ["field1", "field2"])

    # Verify field1 exists and field2 is None
    assert result == {"field1": "value1", "field2": None}


@patch("query_utils.sg_connection")
def test_evaluate_query_fields_entity_not_found(mock_sg):
    # Setup mock to return None (entity not found)
    mock_sg.find_one.return_value = None

    from query_utils import evaluate_query_fields
    result = evaluate_query_fields("Entity", 999, ["field1", "field2"])

    # Verify empty dict is returned
    assert result == {}


@patch("query_utils.evaluate_query_fields")
@patch("query_utils.sg_connection")
def test_get_sequence_query_results(mock_sg_connection,
                                    mock_evaluate_query_fields):
    # Mock sequence return
    mock_sg_connection.find.side_effect = [
        [
            {"id": 101, "code": "Seq_A"}  # Sequences
        ],
        [
            {"id": 201, "code": "Shot_1"},
            {"id": 202, "code": "Shot_2"},
        ]
    ]

    # Mock evaluated query fields
    mock_evaluate_query_fields.side_effect = [
        {"sg_cut_duration": 100, "sg_ip_versions": 2},  # For sequence
        {"sg_cut_duration": 50, "sg_ip_versions": 1},   # For Shot_1
        {"sg_cut_duration": 55, "sg_ip_versions": 1},   # For Shot_2
    ]

    results = get_sequence_query_results(85)

    assert len(results) == 1
    seq = results[0]
    assert seq["name"] == "Seq_A"
    assert seq["sg_cut_duration"] == 100
    assert seq["sg_ip_versions"] == 2
    assert len(seq["shots"]) == 2
    assert seq["shots"][0]["name"] == "Shot_1"
    assert seq["shots"][1]["sg_cut_duration"] == 55


@patch("query_utils.sg_connection")
def test_no_sequences_returns_empty_list(mock_sg_connection):
    mock_sg_connection.return_value = []
    result = get_sequence_query_results(85)
    assert result == []


@patch("query_utils.evaluate_query_fields")
@patch("query_utils.sg_connection")
def test_sequence_with_no_shots(mock_sg_connection,
                                mock_evaluate_query_fields):
    # First call returns sequences, second call returns no shots
    mock_sg_connection.find.side_effect = [
        [
            {"id": 101, "code": "Seq_A"}  # Sequences
        ],
        [
        ]
    ]
    mock_evaluate_query_fields.return_value = {
        "sg_cut_duration": 100,
        "sg_ip_versions": ["v001"]
    }

    result = get_sequence_query_results(85)
    assert len(result) == 1
    assert (result[0]["name"] == "Seq_A")
    assert result[0]["shots"] == []


@patch("query_utils.evaluate_query_fields")
@patch("query_utils.sg_connection")
def test_missing_field_values(mock_find, mock_evaluate_query_fields):
    mock_find.find.side_effect = [
        [{"id": 2, "code": "SEQ_002"}],  # Sequences
        [{"id": 101, "code": "SHOT_001"}],  # Shots
    ]
    # One call for the sequence, one for the shot
    mock_evaluate_query_fields.side_effect = [
        {"sg_cut_duration": None, "sg_ip_versions": None},  # Sequence fields
        {"sg_cut_duration": None, "sg_ip_versions": None},  # Shot fields
    ]

    result = get_sequence_query_results(85)
    assert result[0]['sg_cut_duration'] is None
    assert result[0]['sg_ip_versions'] is None
    assert result[0]['shots'][0]["sg_cut_duration"] is None
    assert result[0]["shots"][0]["sg_ip_versions"] is None


@patch("sg_connection.Shotgun")
def test_shotgrid_connection(mock_shotgun):
    """Test that ShotGridConnector initializes correctly"""
    # Create connector
    sg_conn = ShotGridConnector()
    # Get connection (this should initialize Shotgun)
    sg_conn.get_connection()

    # Assert Shotgun was initialized with correct arguments
    mock_shotgun.assert_called_once_with(
        "https://laika-demo.shotgunstudio.com",
        script_name="code_challenge",
        api_key="2Drsqmdcfhjvfcv%kvxdaqvft",
        connect=True,
        http_proxy=None
    )

# Commented out test with simpler implementation
# def test_connection_failure():
#     """Test that connection failure is handled correctly"""
#     pass
