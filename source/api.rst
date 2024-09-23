REST API
========

List of all methods is available here: https://vk.com/dev/methods.

Executing requests
------------------

.. code-block:: python

    import aiovkcom

    async with aiovkcom.API(v='5.241', access_token='abcde') as vk:
        events = await api.newsfeed.get()

is equivalent to **GET** request:

.. code-blokc:: shell

    GET https://api.vk.com/method/newsfeed.get?access_token=abcde&v=5.241
