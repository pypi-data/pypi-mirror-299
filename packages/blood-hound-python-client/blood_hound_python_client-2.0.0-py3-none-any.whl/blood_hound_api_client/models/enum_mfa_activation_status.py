from enum import Enum


class EnumMfaActivationStatus(str, Enum):
    ACTIVATED = "activated"
    DEACTIVATED = "deactivated"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
