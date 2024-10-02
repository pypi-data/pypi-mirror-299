from enum import Enum


class EnumClientType(str, Enum):
    AZUREHOUND = "azurehound"
    SHARPHOUND = "sharphound"

    def __str__(self) -> str:
        return str(self.value)
