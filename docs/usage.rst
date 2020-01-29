Usage
=====

Once all the desired services have been added, starting a deploy is pretty
straightforward. One API call is used to trigger the deploy and another to
check its status.

Let's say there are two services called `stack_service1` and `stack_service2`.
You can use the following HTTP request to start a deploy.

.. sourcecode:: bash

    $ curl -sSL -X POST '<host>/api/deploy' \
        -H 'Content-Type: application/json' \
        -d '["stack_service1","stack_service2"]'

The request will immediately resolve in a response that looks something like
this:

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json

    {
        "msg": "Task started",
        "task_id": "1be2ef0c636e45169899931df765a8e3"
    }

The task can take an indefinite amount of time and there's no way of knowing
how long. That's where the second endpoint comes in.

.. sourcecode:: bash

    $ curl -sSL '<host>/api/tasks/1be2ef0c636e45169899931df765a8e3'

Which returns

.. sourcecode:: http

    HTTP/1.1 202 ACCEPTED
    Content-Type: application/json

    {
        "msg": "Task is still running"
    }

while the task is still running, and

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "msg": "Successfully updated all services"
    }

When the task has completed successfully.

If any error occured and the stack has been reverted to the previous version,
the response will look like this:

.. sourcecode:: http

    HTTP/1.1 500 INTERNAL SERVER ERROR
    Content-Type: application/json

    {
        "err": "Stack update failed",
        "msg": "Service stack_service1 failed to update. Stack reverted"
    }
