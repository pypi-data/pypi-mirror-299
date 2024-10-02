from enum import Enum


class GetSearchResultType(str, Enum):
    EXACT = "exact"
    FUZZY = "fuzzy"

    def __str__(self) -> str:
        return str(self.value)
