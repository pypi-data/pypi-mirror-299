from enum import Enum


class GetUserEntitySessionsType(str, Enum):
    COUNT = "count"
    GRAPH = "graph"
    LIST = "list"

    def __str__(self) -> str:
        return str(self.value)
