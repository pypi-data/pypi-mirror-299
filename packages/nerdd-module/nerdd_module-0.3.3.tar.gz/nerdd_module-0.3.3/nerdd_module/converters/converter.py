from abc import ABC, abstractmethod
from typing import Any

__all__ = ["Converter"]


class Converter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _convert(self, input: Any, context: dict, **kwargs) -> Any:
        pass

    def convert(self, input: Any, context: dict, **kwargs) -> Any:
        return self._convert(input, context, **kwargs)
