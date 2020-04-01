Getting Started
===============

Installation
------------

If you use pip, just type

.. code-block:: shell

    $ pip install aiovkcom

You can install from the source code like

.. code-block:: shell

    $ git clone https://github.com/KonstantinTogoi/aiovkcom.git
    $ cd aiovkcom
    $ python setup.py install

Account
-------

Sign up in `vk.com <https://vk.com>`_.

Application
-----------

After signing up visit vk.com API
`documentation page <https://vk.com/dev/manuals>`_
and create a new application: https://vk.com/editapp?act=create.

Save **client_id** (aka **app_id**) and **client_secret** (aka **app_secret**)
for user authorization.

.. code-block:: python

    app_id = 'your client id'
    app_secret = 'your secret key'
