from typing import Protocol

from .types import TBuilderOutput, TBuilderListItem
from .partials.with_list.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithList,
)


class BuilderableInterface(
    WithList[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    pass
