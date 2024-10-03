from abc import abstractmethod
from typing import Any, Protocol

from ..with_list.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithListMixin,
)
from ..with_builderable_base.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithBuilderableBaseMixin,
)
from ...types import TBuilderOutput, TBuilderListItem


class BuilderableInterfaceMixin(
    WithListMixin[TBuilderOutput, TBuilderListItem],
    WithBuilderableBaseMixin,
    Protocol[TBuilderOutput, TBuilderListItem],
):
    @abstractmethod
    def build(
        self,
        *args: Any,
        **kwds: Any,
    ) -> TBuilderOutput:
        pass
