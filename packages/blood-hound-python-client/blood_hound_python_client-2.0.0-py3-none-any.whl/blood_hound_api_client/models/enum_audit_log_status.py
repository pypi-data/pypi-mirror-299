from enum import Enum


class EnumAuditLogStatus(str, Enum):
    FAILURE = "failure"
    INTENT = "intent"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
