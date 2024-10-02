from enum import Enum


class GetGpoEntityComputersType(str, Enum):
    COUNT = "count"
    GRAPH = "graph"
    LIST = "list"

    def __str__(self) -> str:
        return str(self.value)
