from typing import Protocol, Self

from ..with_builderable_base.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithBuilderableBaseMixin,
)
from ...types import TBuilderOutput, TBuilderListItem


class BuilderableInterfaceMixin(
    WithBuilderableBaseMixin,
    Protocol[TBuilderOutput, TBuilderListItem],
):
    def get_items(self) -> list[TBuilderListItem]: ...

    def set_items(self, items: list[TBuilderListItem]) -> Self: ...

    def add_item(self, item: TBuilderListItem) -> Self: ...
