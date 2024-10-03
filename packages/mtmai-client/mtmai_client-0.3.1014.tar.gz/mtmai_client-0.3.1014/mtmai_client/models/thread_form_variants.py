from enum import Enum


class ThreadFormVariants(str, Enum):
    CMDK = "cmdk"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
