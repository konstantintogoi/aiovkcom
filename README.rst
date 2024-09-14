.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://github.com/konstantintogoi/aiovkcom/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/aiovkcom.svg
    :target: https://pypi.python.org/pypi/aiovkcom

.. image:: https://img.shields.io/pypi/pyversions/aiovkcom.svg
    :target: https://pypi.python.org/pypi/aiovkcom

.. index-start-marker1

aiovkcom
========

async python `vk.com API <https://dev.vk.com/en/api/api-requests>`_ wrapper
for `REST API <https://dev.vk.com/en/method>`_ methods, see
`documentation <https://konstantintogoi.github.io/aiovkcom>`_.

Example
-------

To use `vk.com API <https://dev.vk.com/en/api/api-requests>`_ you need
an :code:`access_token`.

.. code-block:: python

    import aiovkcom

    async with aiovkcom.API(v='5.241', access_token='your access token') as vk:
        contacts = await vk.account.getContactList()
        friends = await vk.friends.get()
        events = await vk.wall.get()

Installation
------------

.. code-block:: shell

    $ pip install aiovkcom

Supported Python Versions
-------------------------

Python 3.7, 3.8, 3.9 are supported.

.. index-end-marker1

License
-------

aiovkcom is released under the BSD 2-Clause License.
