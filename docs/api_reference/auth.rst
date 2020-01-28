Authentication
--------------

.. http:post:: /api/signup

    .. autosimple:: deploy_webhook.api.auth.create_user

    **Example request**:

    .. sourcecode:: http

        POST /api/signup HTTP/1.1
        Authorization: Bearer eyJ0eXAi...
        Content-Type: application/json

        {
            "username": "admin",
            "password": "admin"
        }


    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
            "msg": "User created",
            "user": {
                "id": 2
                "username": "admin"
            }
        }

.. http:post:: /api/login

    .. autosimple:: deploy_webhook.api.auth.login

    **Example request**:

    .. sourcecode:: http

        POST /api/login HTTP/1.1
        Authorization: Bearer eyJ0eXAi...
        Content-Type: application/json

        {
            "username": "admin",
            "password": "admin"
        }


    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "access_token": "eyJ0eXAi...",
            "refresh_token": "eyJ0eXAi..."
        }

.. http:post:: /api/refresh

    .. autosimple:: deploy_webhook.api.auth.refresh_token

    **Example request**:

    .. sourcecode:: http

        POST /api/refresh HTTP/1.1
        Authorization: Bearer eyJ0eXAi...


    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "access_token": "eyJ0eXAi..."
        }
