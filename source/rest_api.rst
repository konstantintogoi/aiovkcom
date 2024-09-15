REST API
========

List of all methods is available here: https://vk.com/dev/methods.

Executing requests
------------------

.. code-block:: python

    from aiovkcom import API

    api = API(session)

    events = await api.newsfeed.get()  # events for current user
    friends = await api.friends.get()  # current user's friends

Under the hood each API request is enriched
with parameters (https://vk.com/dev/api_requests):

* :code:`access_token`
* :code:`v`

to authorize request.
