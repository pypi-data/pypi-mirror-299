# Suppres

![https://static.pepy.tech/badge/suppress](https://static.pepy.tech/badge/suppress)

Decorator to ignore exceptions. A simple wrapper around contextlib.suppress.

## Install

```
pip install suppress
```

## Usage

```python
import asyncio
from suppress import suppress


@suppress(ZeroDivisionError)
def zero_division_error_function():
    return 1 / 0


@suppress(ZeroDivisionError)
async def zero_division_error_async_function():
    return 1 / 0


async def main():
    zero_division_error_function()
    print('First print')

    await zero_division_error_async_function()
    print('Second print')


if __name__ == '__main__':
    asyncio.run(main())
```
Output:

```
First print
Second print
```
