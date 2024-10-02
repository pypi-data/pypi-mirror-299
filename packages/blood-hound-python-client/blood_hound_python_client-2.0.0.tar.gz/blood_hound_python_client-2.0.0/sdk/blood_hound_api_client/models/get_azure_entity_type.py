from enum import Enum


class GetAzureEntityType(str, Enum):
    GRAPH = "graph"
    LIST = "list"

    def __str__(self) -> str:
        return str(self.value)
