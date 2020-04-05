Session
=======

Request
-------

The session makes **GET** requests when you call methods
of an :code:`API` instance.
For example, the following code block

.. code-block:: python

    from aiovkcom import TokenSession, API

    session = TokenSession('abcde', v='5.101')
    api = API(session)
    news = await api.newsfeed.get()

is equivalent to **GET** request:

.. code-block:: shell

    https://api.vk.com/method/newsfeed.get?access_token=abcde&v=5.101

Response
--------

By default, a session after executing request returns response's body
(value of "response" key).
For example, if original response looks like this:

.. code-block:: python

    {"response":[{"id":210700286,"first_name":"Lindsey","last_name":"Stirling"}]}

then the session will return

.. code-block:: python

    [{"id":210700286,"first_name":"Lindsey","last_name":"Stirling"}]

You can pass :code:`pass_error` parameter to :code:`TokenSession`
for returning original response (including errors).

Error
-----

In case of an error, by default, an exception is raised.
You can pass :code:`pass_error` parameter to :code:`TokenSession`
for returning original error's body.
For example:

.. code-block:: python

    {"error": {"error_code": 1, "error_msg": "Unknown error occurred", "request_params": { ... }}
