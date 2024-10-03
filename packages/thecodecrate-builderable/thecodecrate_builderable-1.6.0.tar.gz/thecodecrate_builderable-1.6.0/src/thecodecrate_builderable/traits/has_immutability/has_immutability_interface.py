from typing import Protocol, Self

from ...types import (
    TBuilderOutput,
    TBuilderListItem,
)
from ...partials.with_list.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithListMixin,
)


class HasImmutabilityInterface(
    WithListMixin[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    def add_item(self, item: TBuilderListItem) -> Self: ...
