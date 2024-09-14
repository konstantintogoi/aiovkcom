# REST API

Methods: [https://dev.vk.com/en/method](https://dev.vk.com/en/method).

## Executing requests

```python
import aiovkcom

async with aiovkcom.API(v='5.241', access_token='abcde') as vk:
    news = await vk.newsfeed.get()
```

is equivalent to **GET** request:

```shell
GET https://api.vk.com/method/newsfeed.get?access_token=abcde&v=5.241
```
