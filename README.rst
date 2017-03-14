=======================
eudat.accounting.server
=======================

Server backend for the EUDAT resource accounting service

An aggregator for accounting records in the EUDAT
Common Data Infrastructure. Records are made to an 
account - typically created per registered (storage)
resource - and accounts can be grouped into domains.
Each domain has its own user base.

This package implements the back-end service. There
is no user interface except for a few primitiv web-based
admin views to create domains, accounts and users.

Record creation is easiest with the accompanying command
line client available from 
https://github.com/EUDAT-DPMT/eudat.accounting.client
but any way to generate a suitble HTTP request will work
(see `Adding Records`_ below).

Accumulated records are available per account in JSON format.


Full documentation and API
==========================

All accumulated data are stored in the schemaless database
ZODB http://www.zodb.org/ made web-accessible by the web 
application server Zope (now largely maintained by the 
Plone community).
The server application itself only provides a few marker
interfaces to which browser views are registered implementing
the functionality needed beyond what Zope provides out-of-the-box

The application is rather minimalistic. So far, there are only
methods for creating and viewing records: ``addRecord`` and
``listRecords`` - to be invoked on accounts - respectively. 
All else needs to be set-up through-the-web. 
This will almost certainly change in the future.


Installation
============

The recommended way to install the service is by using buildout 
within a virtual environment. 

1. Create a virtual environment with a recent version of Python 2.7

2. In there, install ``zc.buildout``:

.. code:: console

  $ bin/pip install zc.buildout

3. Add a buildout configuration file (``buldout.cfg``) to 
the virtualenv folder. An example configuration could look like this:

.. code:: console

  [buildout]
  parts = 
      zeo
      instance
      debug-client
  
  eggs = 
      eudat.accounting.server

  develop = 
      src/eudat.accounting.server
  
  zcml = 
      eudat.accounting.server

  [zeo]
  recipe = plone.recipe.zeoserver

  [instance]
  recipe = plone.recipe.zope2instance 
  user = admin:secret
  zeo-client = on
  shared-blob = on
  eggs = ${buildout:eggs}
  zcml = ${buildout:zcml}

  [debug-client]
  recipe = plone.recipe.zope2instance
  http-address = 8081
  user = admin:secret
  zeo-client = on
  shared-blob = on
  eggs = ${buildout:eggs}
  zcml = ${buildout:zcml}

This example already illustrates how to install two server clients
sharing the same database instance via ZEO. It also shows how to
install the code base of the application direclty from GitHub - 
assuming you have cloned the repository into ``src/``. When 
working with a release, the ``develop`` directive can be skipped.

Running 

.. code:: console

  $ bin/buildout [-v]

will generate the entire application. To run it make sure to
start ZEO first followed by the application server instance:

.. code:: console

  $ bin/zeo start
  $ bin/instance start

Leave the ``debug-client`` alone. It can be useful later when
you want to get interactive access to the database while the
application is running or if you want to invoke server scripts
from the command line while the application is running.

Now point your browser to ``localhost:8080`` (or wherever you
bound the application to) and start configuring your app.

And be sure to change the admin password ;-)
 
Example set-up
==============

First thing to do after completing the steps outlined above is
to create one or several *domains*. This can be achieved in the
ZMI (Zope Management Interface) by adding a ``BTreeFolder`` and
assigning it the marker interface ``eudat.accounting.server.interfaces.IDomain``
available under the ``Interfaces`` tab. It is also recommended to 
add a ``User Folder`` (available from the ``Add`` drop-down)
where you define the users for this domain.

Next, create one or several *accounts* within the domain. Again these
are just ``BTreeFolders`` but this time marked with
``eudat.accounting.server.interfaces.IAccount``

That's it. Now, records can be added to these accouts using 
the client mentioned above and records can be listed by invoking
``<base_url>/<domain_id>/<account_id>/listRecords``

Adding Records
==============

While it is most convenient to add records using one of the clients_
it is also possible to do this *by hand*. One way is to call an
appropriately crafted URL including all data to be transmitted 
like in

.. code:: console

  $ curl -u "probe:<secret>" "http://localhost:8080/demo/12345/addRecord?core.value:record=321&core.unit:record=TB&core.type:record=storage"

This is assuming that you have an accounting service running 
at ``localhost`` on port ``8080`` and a domain called ``demo`` with 
an account ``12345`` and a user ``probe`` with the corresponding 
password ``<secret>``. 
Using the ``:record`` qualifier tells Zope to group the ``type``, ``value``
and ``unit`` into a dictionary called ``core`` as can be seen when 
recalling the data just submitted:

.. code:: console

  $ curl -u "probe:<secret>" http://localhost:8080/demo/12345/listRecords
  [
    {
        "core": {
            "type": "storage",
            "value": "321", 
            "unit": "TB"
        }, 
        "meta": {
            "ts": 1489476898, 
            "submission_time": "2017-03-14 07:34:58"
        }
    }, 
  [...]

Note how the submission time (in UTC) has been added as meta data 
to the record. You can also provide additional meta data yourself
as in 

.. code:: console

  $ curl -u "probe:<secret>" "http://localhost:8080/demo/12345/addRecord?core.value:record=321&core.unit:record=TB&core.type:record=storage&meta.comment:record=This+is+a+demo"

resulting in 

.. code:: console

  $ curl -u "probe:http://localhost:8080/demo/12345/listRecords
  [
    {
        "core": {
            "type": "storage",
            "value": "325", 
            "unit": "TB"
        }, 
        "meta": {
            "comment": "This is a comment", 
            "ts": 1489477707, 
            "submission_time": "2017-03-14 07:48:27"
        }
    }, 
  [..]

Note that you have to take care that data are encoded correctly yourself.

With respect to the keys supported (``value``, ``unit``, ``comment``) and
the grouping (what goes into ``core`` and what goes into ``meta``) you 
are completely free to use whatever you want thereby implementing
any policy you like.

In EUDAT, we have adopted the convention that ``core`` needs to have 
a ``value``, a ``unit`` and a ``type`` whereas everything in ``meta`` is
optional. You can look at the clients_ if you want to see this 
demonstrated further. 




.. _clients: https://github.com/EUDAT-DPMT/eudat.accounting.client 


Developer notes
===============

Please use a virtualenv to maintain this package, but I should not need to say that.

The installation instructions above already show how to setup 
a development environment.

Links
=====

Project home page

  https://github.com/EUDAT-DPMT/eudat.accounting.server

Source code

  https://github.com/EUDAT-DPMT/eudat.accounting.server

Issues tracker

  https://github.com/EUDAT-DPMT/eudat.accounting.server/issues

