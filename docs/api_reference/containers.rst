Containers
----------

.. http:post:: /api/containers/(container_short_id)/exec

    .. autosimple:: deploy_webhook.api.containers.exec_command

    **Example request**:

    .. sourcecode:: http

        POST /api/containers/17db9ee7ac/exec HTTP/1.1
        Authorization: Bearer eyJ0eXAi...

        {
            "commands": ["echo test", "uname"]
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "msg": "Successfully ran commands",
            "result": [
                {
                    "code": 0,
                    "command": "echo test",
                    "output": "test\n"
                },
                {
                    "code": 0,
                    "command": "uname",
                    "output": "Linux\n"
                }
            ]
        }

.. http:get:: /api/containers/(container_short_id)/logs

    .. autosimple:: deploy_webhook.api.containers.get_container_logs

    **Example request**:

    .. sourcecode:: http

        GET /api/containers/17db9ee7ac/logs HTTP/1.1
        Authorization: Bearer eyJ0eXAi...

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "container_name": "stack_service.1.w8bxr...",
            "msg": "Successfully grabbed logs",
            "output": "hello world\n"
        }
