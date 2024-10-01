from __feature__ import snake_case

import os
from typing import Union, Any


class _RegistryConnector:

    def __init__(self, registry: Union[dict, "BaseRegistry"] = None):
        self._registry = registry or {}

    def data(self, *args, **kwargs) -> Any:
        return None

    def set_registry(self, registry: Union[dict, "BaseRegistry"] = None):
        self._registry = registry

    def update(self, *args, **kwargs):
        raise NotImplementedError(f"Method `{self.__qualname__}` must be implemented")


class _DataFileConnector(_RegistryConnector):

    def data(self, filename: str) -> Any:
        return self._registry.get(filename)

    def update(self, icons: dict[str, Union[str, os.PathLike]]):
        self._registry.update(**icons)

    def __call__(self, filename: str) -> Any:
        return self._registry.get(filename)


DataFile = _DataFileConnector()


class _ThemeFileConnector(_RegistryConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_sheet = ""

    def data(self) -> Any:
        return self._style_sheet

    def update(self, filename: Union[str, os.PathLike]):
        with open(filename, "r", encoding="utf-8") as output:
            self._style_sheet += output.read()


ThemeFile = _ThemeFileConnector()
