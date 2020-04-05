.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://github.com/KonstantinTogoi/aiovkcom/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/aiovkcom.svg
    :target: https://pypi.python.org/pypi/aiovkcom

.. image:: https://img.shields.io/pypi/pyversions/aiovkcom.svg
    :target: https://pypi.python.org/pypi/aiovkcom

.. image:: https://readthedocs.org/projects/aiovkcom/badge/?version=latest
    :target: https://aiovkcom.readthedocs.io/en/latest/

.. image:: https://travis-ci.com/KonstantinTogoi/aiovkcom.svg
    :target: https://travis-ci.com/KonstantinTogoi/aiovkcom

.. index-start-marker1

aiovkcom
========

aiovkcom is a python `vk.com API <https://vk.com/dev/api_requests>`_ wrapper.
The main features are:

* authorization (`Authorization Code <https://oauth.net/2/grant-types/authorization-code/>`_, `Implicit Flow <https://oauth.net/2/grant-types/implicit/>`_)
* `REST API <https://vk.com/dev/methods>`_ methods

Usage
-----

To use `vk.com API <https://vk.com/dev/api_requests>`_ you need
a registered app and `vk.com <https://vk.com>`_ account.
For more details, see
`aiovkcom Documentation <https://aiovkcom.readthedocs.io/>`_.

.. code-block:: python

    from aiovkcom import TokenSession, API

    session = TokenSession(access_token, v='5.101')
    api = API(session)

    events = await api.wall.get()
    friends = await api.friends.get()

Pass :code:`access_token` that was received after authorization.
For more details, see
`aiovkcom Documentation <https://aiovkcom.readthedocs.io/>`_.

Installation
------------

.. code-block:: shell

    $ pip install aiovkcom

or

.. code-block:: shell

    $ python setup.py install

Supported Python Versions
-------------------------

Python 3.5, 3.6, 3.7 and 3.8 are supported.

.. index-end-marker1

Test
----

Run all tests.

.. code-block:: shell

    $ python setup.py test

Run tests with PyTest.

.. code-block:: shell

    $ python -m pytest [-k TEST_NAME]

License
-------

aiovkcom is released under the BSD 2-Clause License.
