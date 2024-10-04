from pathlib import Path
from typing import Callable

from click import Choice


class LazyChoice(Choice):
    def __init__(self, getter: Callable, case_sensitive: bool = True):
        super().__init__([], case_sensitive=case_sensitive)
        self.getter = getter

    @property
    def choices(self):
        return self.getter()

    @choices.setter
    def choices(self, v):
        pass


def to_windows_path(path: Path) -> str:
    return "C:\\" + str(path).replace("/", "\\")
