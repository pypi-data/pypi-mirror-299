from enum import Enum


class GetPlatformDataQualityAggregatePlatformId(str, Enum):
    AD = "ad"
    AZURE = "azure"

    def __str__(self) -> str:
        return str(self.value)
