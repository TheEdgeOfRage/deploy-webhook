Services
--------

.. http:get:: /api/services

    .. autosimple:: deploy_webhook.api.services.get_services

    **Example request**:

    .. sourcecode:: http

        GET /api/services HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJK...

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "msg": "Task started",
            "services": [
                {
                    "name": "stack_service",
                    "repository": "user/repo",
                    "tag": "latest",
                    "active": true,
                    "containers": [
                        {
                            "status": "running",
                            "short_id": "17db9ee7ac",
                            "name": "stack_service.1.w8bxr...",
                            "id": "17db9ee7ac179fe..."
                        }
                    ]
                }
            ]
        }

.. http:post:: /api/services

    .. autosimple:: deploy_webhook.api.services.add_service

    **Example request**:

    .. sourcecode:: http

        POST /api/deploy HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJK...
        Content-Type: application/json

        {
            "name": "stack_service",
            "repository": "user/repo",
            "tag": "latest"
        }


    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
            "msg": "Successfully added service",
            "service": {
                "name": "stack_service",
                "repository": "user/repo",
                "tag": "latest"
            }
        }

.. http:delete:: /api/services/(service_name)

    .. autosimple:: deploy_webhook.api.services.delete_service

    **Example request**:

    .. sourcecode:: http

        DELETE /api/services/stack_service HTTP/1.1
        Authorization: Bearer eyJ0eXAiOiJK...

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "msg": "Successfully deleted service named stack_service"
        }
