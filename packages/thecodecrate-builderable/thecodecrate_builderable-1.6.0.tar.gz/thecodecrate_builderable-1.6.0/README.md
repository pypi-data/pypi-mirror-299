# Python-Builderable

Builderable is a modular class for implementing the Builder pattern in Python.

The library is designed to allow developers to compose builder classes using pre-defined partials (mixins) or implement their own.

## Installation

```bash
pip install thecodecrate-builderable
```

## Usage Example

Here's a simple example of how to implement a builder class with builderable:

```python
from builderable import Builderable, WithListMixin

class MyBuilder(Builderable[int]):
    def build(self) -> int:
        return sum(self.get_items())

# Usage
builder = MyBuilder()
result = builder.add_item(5).add_item(10).build()
print(result)  # Outputs: 15
```

## Immutability Trait

In some cases, you may want to enforce immutability, meaning each modification creates a new instance of the builder, rather than modifying the current one. This can be achieved by including the immutability trait in your builder class.

When using the `HasImmutability` trait, methods like "add_item" will clone the self object, append the new item to the clone's list, and return the cloned object. Without this trait, "add_item" will modify the current object directly.

Here's how to use the immutability feature:

```python
class ImmutableBuilder(
    HasImmutability[int, int],  # Enforces immutability
    Builderable[int, int],
):
    def build(self) -> int:
        return sum(self.get_items())

# Usage
builder = (ImmutableBuilder()).add_item(5).add_item(10)

# The original builder remains unchanged
new_builder = builder.add_item(7)
print(new_builder.get_items())  # Outputs: [5, 10, 7]
print(builder.get_items())  # Outputs: [5, 10]
```

## License

This project is licensed under the MIT License.
