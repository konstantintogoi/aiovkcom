# Requests

`aiovkcom` executes http requests with `httpx.AsyncClient`.

## Request Format

`httpx.AsyncClient` makes **GET** requests according to
[Request Format](https://dev.vk.com/en/api/api-requests).
For example:

```shell
GET https://api.vk.com/method/newsfeed.get?access_token=abcde&v=5.241
```

## Response Format

```python
{
    "response": ...
}
```

or

```python
{
    "error": {
        "error_code": 1,
        "error_msg": "Unknown error occurred",
        "request_params": { ... }
    }
}
```
