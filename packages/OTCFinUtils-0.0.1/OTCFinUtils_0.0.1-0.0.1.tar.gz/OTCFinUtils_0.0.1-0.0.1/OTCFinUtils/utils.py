import re
import json
from typing import Optional

def extract_segment_object_line(lines: list[str]) -> str:
    for line in lines:
        if "@odata.context" in line:
            return line
    raise ValueError("Object line not found in batch response.")


def extract_segment_response_id(lines: list[str], id_column: str) -> Optional[str]:
    """
    From a list of lines of a batch response, returns 
    the id of the entity in the response. If a null
    id column name is provided, return None.
    """
    try:
        if not id_column:
            return None

        object_line = extract_segment_object_line(lines)
        json_object = json.loads(object_line)
        object_id: str = json_object[id_column]

        return object_id
    
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON error in response id logic: {e}")
    except KeyError as e:
        raise RuntimeError(f"Key error in response id logic: {e}")
    except Exception as e:
        raise RuntimeError(f"Error in response id logic: {e}")


def extract_segment_status_code(lines: list[str]) -> int:
    """
    From a list of lines of a batch response,
    returns the HTTP status code.
    """
    status_code_line = lines[4]
    status_code_line_parts = status_code_line.split(" ")
    status_code = status_code_line_parts[1]
    status_code = int(status_code)
    
    return status_code


def extract_segment_table_name(lines: list[str]) -> str:
    """
    From a list of lines of a batch response,
    returns the table name of the entity using regex.
    """
    object_line = extract_segment_object_line(lines)
    pattern = r'metadata#([a-z0-9_]+)'
    pattern_matches = re.findall(pattern, object_line)
    
    if not pattern_matches:
        raise RuntimeError(f"Could not find table pattern in string: {object_line}")
    
    table = pattern_matches[0]
    return table