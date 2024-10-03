from typing import Protocol

from .builderable_interface import BuilderableInterface
from .types import TBuilderOutput, TBuilderListItem
from .partials.with_list.builderable_mixin import BuilderableMixin as WithList


class Builderable(
    WithList[TBuilderOutput, TBuilderListItem],
    BuilderableInterface[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    def __init__(self) -> None:
        self.set_items([])
