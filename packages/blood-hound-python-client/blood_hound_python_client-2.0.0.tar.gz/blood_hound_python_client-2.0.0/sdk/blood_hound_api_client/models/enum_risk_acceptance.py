from enum import Enum


class EnumRiskAcceptance(str, Enum):
    ACCEPTED = "accepted"
    ALL = "all"
    UNACCEPTED = "unaccepted"
    VALUE_3 = ""

    def __str__(self) -> str:
        return str(self.value)
