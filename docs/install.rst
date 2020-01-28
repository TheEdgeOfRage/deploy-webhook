Installation
============

**deploy-webhook** can be installed either on the host machine directly,
or run as a Docker container with access to the host docker socket.

Start off by cloning the repository to your preferred location:

.. code-block:: bash

    $ git clone https://github.com/TheEdgeOfRage/deploy-webhook

Docker installation
-------------------

There is already a production-ready docker-compose.yml file in this repo.
Two variables need to be set in a .env file or hardcoded in the compose file:

- `SECRET_KEY` (The key used to sign JWT tokens)

To start the app, just run:

.. code-block:: bash

    $ docker-compose up -d

It will build the image, start the container in the background,
and expose the app on the configured port.


Host installation
-----------------

A few environment variables need to be set in order for the app to run:

- `SECRET_KEY=default-key` (The key used to sign JWT tokens)
- `SQLALCHEMY_DATABASE_URI=/path/to/auth.db`

Install all of the required dependencies using Poetry:

.. code-block:: bash

    $ poetry install

Before running the app, the database tables need to be created:

.. code-block:: bash

    $ poetry run flask db upgrade
    $ poetry run gunicorn --bind 0.0.0.0:<PORT> run:app

The user who runs the app must have write access to the docker socket to
be able to manage containers and services.
