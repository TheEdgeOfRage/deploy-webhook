Deployment
----------

.. http:post:: /api/deploy

    .. autosimple:: deploy_webhook.api.deploy.deploy

    **Example request**:

    .. sourcecode:: http

        POST /api/deploy HTTP/1.1
        Content-Type: application/json

        {
            "services": ["stack_service"]
        }


    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 202 ACCEPTED
        Content-Type: application/json

        {
            "msg": "Task started",
            "task_id": "1be2ef0c636e45169899931df765a8e3"
        }


.. http:get:: /api/tasks/(task_id)

    .. autosimple:: deploy_webhook.api.tasks.get_task_status

    **Example request**:

    .. sourcecode:: http

        GET /api/tasks/1be2ef0c636e45169899931df765a8e3 HTTP/1.1
        Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "msg": "Successfully updated all services"
        }
