from typing import Protocol, Self

from .builderable_interface_mixin import BuilderableInterfaceMixin
from ...types import TBuilderOutput, TBuilderListItem


class BuilderableMixin(
    BuilderableInterfaceMixin[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    _items: list[TBuilderListItem] = []

    def get_items(self) -> list[TBuilderListItem]:
        return self._items

    def set_items(self, items: list[TBuilderListItem]) -> Self:
        self._items = items

        return self

    def add_item(self, item: TBuilderListItem) -> Self:
        self.get_items().append(item)

        return self
