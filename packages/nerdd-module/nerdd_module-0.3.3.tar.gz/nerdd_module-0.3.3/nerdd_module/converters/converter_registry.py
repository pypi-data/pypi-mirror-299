from functools import lru_cache, partial
from typing import Callable, Dict, Tuple, Type

from ..util import call_with_mappings, class_decorator
from .converter import Converter
from .identity_converter import IdentityConverter

__all__ = [
    "ConverterRegistry",
    "register_representation",
]


ConverterFactory = Callable[[dict], Converter]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ConverterRegistry:
    def __init__(self) -> None:
        self._factories: Dict[Tuple[str, str], ConverterFactory] = {}

    def register(
        self,
        data_type: str,
        output_format: str,
        ConverterClass: Type[Converter],
        *args: str,
        **kwargs: str,
    ):
        assert issubclass(ConverterClass, Converter)
        assert all([isinstance(arg, str) for arg in args])
        assert all(
            [isinstance(k, str) and isinstance(v, str) for k, v in kwargs.items()]
        )

        self._factories[(data_type, output_format)] = partial(
            call_with_mappings, ConverterClass, args_mapping=args, kwargs_mapping=kwargs
        )

    def get_converter(
        self, data_type: str, output_format: str, return_default=True, **kwargs
    ) -> Converter:
        if (data_type, output_format) not in self._factories:
            if return_default:
                return IdentityConverter()
            else:
                raise ValueError(
                    f"Unknown data type '{data_type}' or output format '{output_format}'"
                )
        return self._factories[(data_type, output_format)](kwargs)

    def get_output_formats(self) -> frozenset:
        return frozenset(self._factories.keys())


@class_decorator
def register_representation(
    cls: Type[Converter], data_type: str, output_format: str, *args, **kwargs
):
    ConverterRegistry().register(data_type, output_format, cls, *args, **kwargs)
