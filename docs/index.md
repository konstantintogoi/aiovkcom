[![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/konstantintogoi/aiovkcom/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/pypi/v/aiovkcom.svg)](https://pypi.python.org/pypi/aiovkcom)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/aiovkcom.svg)](https://pypi.python.org/pypi/aiovkcom)

# aiovkcom

async python [vk.com API](https://dev.vk.com/en/api/api-requests) wrapper
for [REST API](https://dev.vk.com/en/method) methods, see
[documentation](https://konstantintogoi.github.io/aiovkcom).

## Example

To use [vk.com API](https://dev.vk.com/en/api/api-requests) you need an `access_token`.

```python
import aiovkcom

async with aiovkcom.API(v='5.241', access_token='your access token') as vk:
    contacts = await vk.account.getContactList()
    friends = await api.friends.get()
    events = await api.wall.get()
```

## Installation

```shell
$ pip install aiovkcom
```

## Supported Python Versions

Python 3.7, 3.8, 3.9 are supported.

## License

aiovkcom is released under the BSD 2-Clause License.
