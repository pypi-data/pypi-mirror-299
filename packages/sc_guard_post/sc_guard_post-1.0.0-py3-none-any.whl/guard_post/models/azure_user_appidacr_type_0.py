from enum import Enum


class AzureUserAppidacrType0(str, Enum):
    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_2 = "2"

    def __str__(self) -> str:
        return str(self.value)
