# vk.com Python REST API wrapper

- [About](#about)
- [Getting Started](#getting-started)


## About

This is a [vk.com](https://vk.com) (Russian social network) python API wrapper.
The goal is to support all API methods: https://vk.com/dev/methods.


## Getting Started

Install package using pip

```bash
pip install aiovkcom
```

To use VK API you need a registered app and login account in the social network.

1. Sign up in [vk.com](https://vk.com)
2. Create **standalone** application.
3. Save **App ID**.
4. Use App ID, list of required permissions and user credentials to get **access token**.
5. Use the access token to make method requests.

After signing up go to https://vk.com/dev/standalone and create application.

```python
app_id = 'your App ID'
```

### ImplicitSession

You can authenticate with [VK API OAuth2](https://vk.com/dev/implicit_flow_user) by passing user credentials and permissions to `ImplicitSession`.

```python
from aiovkcom import ImplicitSession
from aiovkcom.permissions import bit_scope, PERMISSIONS

phone = '+1999123456'
password = 'user password'

session = await ImplicitSession(
    app_id=app_id,
    login=phone,  # set phone number or e-mail as login
    passwd=password,
    scope=bit_scope(PERMISSIONS),  # get all possible permissions
    v='5.101',  # set version for all requests
)
```

List of all permissions is available here: https://vk.com/dev/permissions.

Now you can execute API requests (see [Executing API requests](#executing-api-requests)). After authentication you will get access token **session.access_token**. Save it to make requests later:

```python
access_token = session.access_token
```

### TokenSession

If you already have an access token you can instantiate `TokenSession`

```python
from aiovkcom import TokenSession

session = TokenSession(access_token, v='5.101')
```

and execute requests.

### Executing API requests

List of all methods is available here: https://vk.com/dev/methods.

```python
from aiovkcom import API

api = API(session)

# current user's friends
friends = await api.friends.get()

# current user's groups
groups = await api.groups.get()
```

List of objects is available here: https://vk.com/dev/objects

## License

**aiovkcom** is released under an BSD 2-Clause License.
