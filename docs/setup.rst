Initial setup
=============

The app exposes a simple CLI through the flask click integration, so any
administrative changes can be made that way, or through the API directly.
At the very least an initial admin user needs to be created with the CLI.

If Docker is used to run the app, any CLI commands need to be run inside
the container. If docker-compose is used, prefixing them with
`docker-compose exec webhoook` should be enough.

Create user
-----------

**CLI:**

.. sourcecode:: bash

    # non-interactive
    $ flask seed user -u <username> -p <password>

    # interactive
    $ flask seed user -u <username> --prompt

    # help
    $ flask seed user --help

**API:**

.. sourcecode:: bash

    $ curl -sSL -X POST '<host>/api/signup' \
        -H 'Authorization: Bearer <token>' \
        -H 'Content-Type: application/json' \
        -d '{"username":"<username>","password":"<password>"}'

For information about how to get the JWT token, refer to the API reference.

Add service
-----------

To be able to update services, they have to be tracked by the app. Tracking
means registering the service name and the image that is used to update
it with the app.

**CLI:**

.. sourcecode:: bash

    # track service
    $ flask seed service -n <service_name> -r <image_repository> -t <image_tag>

    # help
    $ flask seed service --help

**API:**

.. sourcecode:: bash

    $ curl -sSL -X POST '<host>/api/services' \
        -H 'Authorization: Bearer <token>' \
        -H 'Content-Type: application/json' \
        -d '{
            "name":"<service_name>",
            "repository":"<image_repository>",
            "tag":"<image_tag>"
        }'
