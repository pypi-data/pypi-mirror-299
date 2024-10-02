from enum import Enum


class EnumDatapipeStatus(str, Enum):
    ANALYZING = "analyzing"
    IDLE = "idle"
    INGESTING = "ingesting"

    def __str__(self) -> str:
        return str(self.value)
