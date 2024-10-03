import copy
from typing import Protocol, Self

from .has_immutability_interface import HasImmutabilityInterface
from ...types import (
    TBuilderOutput,
    TBuilderListItem,
)


class HasImmutability(
    HasImmutabilityInterface[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    def add_item(self, item: TBuilderListItem) -> Self:
        cloned = copy.deepcopy(self)

        cloned.get_items().append(item)

        return cloned
