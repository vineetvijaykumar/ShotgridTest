from sg_connection import ShotGridConnector
from typing import List, Dict, Any

try:
    sg_connection = ShotGridConnector().get_connection()
    print('Connection Found', sg_connection)
except Exception as e:
    raise Exception('Connection to ShotGrid failed: {}'.format(e))

def evaluate_query_fields(entity_type: str, entity_id: int, field_names: List[str]) -> Dict[str, Any]:
    """
    Evaluates and returns the values of multiple ShotGrid query fields without
    knowing the filter conditions in advance.

    Args:
        entity_type (str): The type of entity to query (e.g., "Sequence").
        entity_id (int): The ID of the entity to query.
        field_names (List[str]): A list of query field names to evaluate.

    Returns:
        Dict[str, Any]: A dictionary mapping each field name to its evaluated value.
                        Returns an empty dict if the entity is not found.
    """
    result = sg_connection.find_one(
        entity_type,
        [["id", "is", entity_id]],
        field_names
    )

    return {field: result.get(field) for field in field_names} if result else {}

def get_sequence_query_results(project_id: int):
    """
    Retrieves all Sequences for a given project and evaluates specified query fields.

    Args:
        project_id (int): The ID of the ShotGrid project.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing sequence name and query field values.
    """
    query_fields = ["sg_cut_duration", "sg_ip_versions"]

    sequences = sg_connection.find(
        "Sequence",
        [["project", "is", {"type": "Project", "id": project_id}]],
        ["id", "code"]
    )

    results = []
    for seq in sequences:
        field_values = evaluate_query_fields("Sequence", seq["id"], query_fields)
        result = {
            "name": seq["code"],
            **field_values
        }
        results.append(result)

    return results

print (get_sequence_query_results(85))