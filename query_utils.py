from typing import List, Dict, Any

from sg_connection import ShotGridConnector

try:
    sg_connection = ShotGridConnector().get_connection()
    print('Connection Found', sg_connection)
except Exception as e:
    raise Exception('Connection to ShotGrid failed: {}'.format(e))


def evaluate_query_fields(entity_type: str, entity_id: int,
                          field_names: List[str]) -> Dict[str, Any]:
    """
    Evaluates and returns the values of multiple ShotGrid query fields without
    knowing the filter conditions in advance.

    Args:
        entity_type (str): The type of entity to query (e.g., "Sequence").
        entity_id (int): The ID of the entity to query.
        field_names (List[str]): A list of query field names to evaluate.

    Returns:
        Dict[str, Any]: A dictionary mapping each field name to its evaluated
            value. Returns an empty dict if the entity is not found.
    """
    result = sg_connection.find_one(
        entity_type,
        [["id", "is", entity_id]],
        field_names
    )

    return ({field: result.get(field) for field in field_names}
            if result else {})


def get_sequence_data(project_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all Sequences for a given project and evaluates specified query
    fields.

    Args:
        project_id (int): The ID of the ShotGrid project.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing sequence name
            and query field values, with an empty 'shots' list to be populated
            later.
    """
    query_fields = ["sg_cut_duration", "sg_ip_versions"]

    sequences = sg_connection.find(
        "Sequence",
        [["project", "is", {"type": "Project", "id": project_id}]],
        ["id", "code"]
    )

    results = []
    for seq in sequences:
        seq_fields = evaluate_query_fields("Sequence", seq["id"], query_fields)
        sequence_data = {
            "id": seq["id"],
            "name": seq["code"],
            **seq_fields,
            "shots": []
        }
        results.append(sequence_data)

    return results


def get_shots_for_sequence(sequence_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves all Shots for a given Sequence and evaluates specified query
    fields.

    Args:
        sequence_id (int): The ID of the ShotGrid sequence.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing shot name and
            query field values.
    """
    query_fields = ["sg_cut_duration", "sg_ip_versions"]

    shots = sg_connection.find(
        "Shot",
        [["sg_sequence", "is", {"type": "Sequence", "id": sequence_id}]],
        ["id", "code"]
    )

    shot_data = []
    for shot in shots:
        shot_fields = evaluate_query_fields("Shot", shot["id"], query_fields)
        shot_data.append({
            "name": shot["code"],
            **shot_fields
        })

    return shot_data


def get_sequence_query_results(project_id: int) -> List[Dict[str, Any]]:
    """
    Combines sequence and shot query field data into a unified nested
    structure.

    Args:
        project_id (int): The ID of the ShotGrid project.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing sequence data
    """
    sequences = get_sequence_data(project_id)

    for seq in sequences:
        seq["shots"] = get_shots_for_sequence(seq["id"])

    return sequences
