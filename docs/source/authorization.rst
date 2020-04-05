Authorization
=============

To authorize with vk.com OAuth 2.0 you need :code:`app_id` (Implicit Grant)
or :code:`app_id` and :code:`app_secret` (Code Grant).

The preferred way to authorize is an :code:`async with` statement.
After authorization the session will have the following attributes:

* :code:`access_token`
* :code:`expires_in`
* :code:`user_id`

Authorization Code Grant
------------------------

.. code-block:: python

    from aiovkcom import CodeSession, API

    app_id = 123456
    app_secret = 'abc'

    async with CodeSession(app_id, app_secret, code, redirect_uri) as session:
        api = API(session)
        ...

About OAuth 2.0 Authorization Code Grant: https://oauth.net/2/grant-types/authorization-code/

For more details, see https://vk.com/dev/authcode_flow_user

Implicit Grant
--------------

.. code-block:: python

    from aiovkcom import ImplicitSession, API

    app_id = 123456
    app_secret = ''

    async with ImplicitSession(app_id, login, passwd, scope) as session:
        api = API(session)
        ...

About OAuth 2.0 Implicit Grant: https://oauth.net/2/grant-types/implicit/

For more details, see https://vk.com/dev/implicit_flow_user
