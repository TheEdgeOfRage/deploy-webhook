==============
Deploy webhook
==============

A Flask app to manage Docker stack deployments.

Best in conjuction with https://github.com/TheEdgeOfRage/deploy-app.

Under the hood, deploy-webhook uses servicectl_ to manage the services.
It's a python library that acts as a frontend to the `Python Docker library
<https://github.com/docker/docker-py>`_ with some additional functionality
allowing eg. the atomic stack updates.

.. _servicectl: https://github.com/TheEdgeOfRage/servicectl

Documentation
=============

The documentation with a setup guide can be found at
https://docs.theedgeofrage.com/deploy-webhook.

License
=======

This software is distributed under terms of the BSD-3-Clause license.

Credits
=======

The async task runner is based on @miguelgrinberg's code from the
flack_ repository.

.. _flack: https://github.com/miguelgrinberg/flack
