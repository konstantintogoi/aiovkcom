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

A session after executing request returns response's body. Example:

.. code-block:: python

    {"response":[{"id":210700286,"first_name":"Lindsey","last_name":"Stirling"}]}

Error
-----

In case of an error, by default, an exception is raised.
You can pass :code:`raise_for_status=False` parameter to :code:`TokenSession`
for returning original response. Example:

.. code-block:: python

    {"error": {"error_code": 1, "error_msg": "Unknown error occurred", "request_params": { ... }}
