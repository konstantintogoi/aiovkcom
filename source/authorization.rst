Authorization
=============

To authorize with vk.com OAuth 2.0 you need
:code:`app_id` and :code:`app_secret` (Code Grant).

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

About OAuth 2.0 Authorization Code Grant: https://oauth.net/2/grant-types/authorization-code/.

For more details, see https://vk.com/dev/authcode_flow_user.
