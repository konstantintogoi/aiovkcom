Requests
========

:code:`aiovkcom` executes http requests with :code:`httpx.AsyncClient`.

Request Format
--------------

:code:`httpx.AsyncClient` makes **GET** requests according to
`Request Format <https://dev.vk.com/en/api/api-requests>`_.
For example:

.. code-block:: shell

    GET https://api.vk.com/method/newsfeed.get?access_token=abcde&v=5.241

Response Format
---------------

.. code-block:: python

    {
        "response": ...
    }

or

.. code-block:: python

    {
        "error": {
            "error_code": 1,
            "error_msg": "Unknown error occurred",
            "request_params": { ... },
    }
