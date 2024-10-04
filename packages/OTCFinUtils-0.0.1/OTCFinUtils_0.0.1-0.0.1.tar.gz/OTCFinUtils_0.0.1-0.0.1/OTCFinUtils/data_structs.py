from enum import Enum
from dataclasses import dataclass

@dataclass
class ResponseIds:
    """
    Used as a return value from the upsert operation on the DV.
    Contains the table names and ids of the entities that were 
    updated and created, stored separately.
    """
    def __init__(self) -> None:
        self.updated_entity_ids: dict[str, set[str]] = dict()
        self.created_entity_ids: dict[str, set[str]] = dict()

    
    def append(self, status_code: int, id: str, table: str) -> None:
        """
        Depending on the status code appends the id and 
        table name to the create / update category.
        """
        if status_code == HTTPStatus.OK.value and table in self.updated_entity_ids:
            self.updated_entity_ids[table].add(id)
        
        elif status_code == HTTPStatus.OK.value and table not in self.updated_entity_ids:
            self.updated_entity_ids[table] = set()
            self.updated_entity_ids[table].add(id)
        
        elif status_code == HTTPStatus.CREATED.value and table in self.created_entity_ids:
            self.created_entity_ids[table].add(id)
        
        elif status_code == HTTPStatus.CREATED.value and table not in self.created_entity_ids:
            self.created_entity_ids[table] = set()
            self.created_entity_ids[table].add(id)
        
        return
    

    def merge(self, delta_ids: "ResponseIds") -> None:
        """
        Merges the values from the provided object onto the
        the values of the calling object.
        """
        for table, ids in delta_ids.created_entity_ids.items():
            if table not in self.created_entity_ids:
                self.created_entity_ids[table] = set()
            self.created_entity_ids[table].update(ids)

        for table, ids in delta_ids.updated_entity_ids.items():
            if table not in self.updated_entity_ids:
                self.updated_entity_ids[table] = set()
            self.updated_entity_ids[table].update(ids)

        return
    

    def json_updated_entities(self) -> dict[str, list]:
        """
        Used for getting a JSON compatible object.
        """
        result = dict()
        for table, ids in self.updated_entity_ids.items():
            result[table] = list(ids)
        return result
    

    def json_created_entities(self) -> dict[str, list]:
        """
        Used for getting a JSON compatible object.
        """
        result = dict()
        for table, ids in self.created_entity_ids.items():
            result[table] = list(ids)
        return result
    

    def __str__(self) -> str:
        return (
            f"created: {self.created_entity_ids}\n"
            f"updated: {self.updated_entity_ids}"
        )
    

@dataclass
class APIParams:
    """
    Basic helper data structure for making API calls.
    """
    url: str
    method: str
    data: dict | None = None


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HTTPStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500