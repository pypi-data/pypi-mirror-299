from .builderable import Builderable
from .types import TBuilderOutput, TBuilderListItem
from .partials.with_build_method.builderable_mixin import (
    BuilderableMixin as WithBuildMethod,
)
from .partials.with_build_method.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithBuildMethodInterface,
)
from .partials.with_builderable_base.builderable_mixin import (
    BuilderableMixin as WithBuilderableBase,
)
from .partials.with_builderable_base.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithBuilderableBaseInterface,
)
from .partials.with_list.builderable_mixin import (
    BuilderableMixin as WithList,
)
from .partials.with_list.builderable_interface_mixin import (
    BuilderableInterfaceMixin as WithListInterface,
)
from .traits.has_immutability.has_immutability import (
    HasImmutability,
)
from .traits.has_immutability.has_immutability_interface import (
    HasImmutabilityInterface,
)


# Version of the package
# DO NOT MODIFY MANUALLY
# This will be updated by `bumpver` command.
# - Make sure to commit all changes first before running `bumpver`.
# - Run `bumpver update --[minor|major|patch]`
__version__ = "1.6.0"

# Expose the public API
__all__ = [
    # Core
    "Builderable",
    "TBuilderOutput",
    "TBuilderListItem",
    # Partials
    "WithBuildMethod",
    "WithBuildMethodInterface",
    "WithBuilderableBase",
    "WithBuilderableBaseInterface",
    "WithList",
    "WithListInterface",
    # Traits
    "HasImmutability",
    "HasImmutabilityInterface",
]
