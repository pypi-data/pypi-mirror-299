from typing import Protocol

from .builderable_interface_mixin import BuilderableInterfaceMixin
from ...types import TBuilderOutput, TBuilderListItem


class BuilderableMixin(
    BuilderableInterfaceMixin[TBuilderOutput, TBuilderListItem],
    Protocol[TBuilderOutput, TBuilderListItem],
):
    pass
