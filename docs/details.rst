Details
=======

A word on synchronicity
-----------------------

Most endpoints are only meant to be used from the frontend, as they have no
practical value as pure JSON API endpoints.

The two endpoints that are meant to be used as an API are `/deploy` and
`/tasks`.

As `/deploy` is an asynchronous endpoint, it doesn't wait until the request
is completed before returning a response. Instead, it spins up a separate
task thread and assigns it a unique `task_id` which in turn gets returned as
the response.

Since there is no way of knowing how long the task will take, there exists the
`/tasks` endpoint. It is used to check the status of a task, by its id. It
returns either a 202 status if the task hasn't finished yet, or the response
from the task if it has.

As of now, the `/deploy` endpoint is the only asynchronous one, but that may
change in the future. Nevertheless, the task interface will stay the same, as
it's universal.

How are services deployed
-------------------------

So how does the service deployment actually work then? When a deploy is
triggered, the request body contains a list of all the services that are to
be updated. A intersection between that list and the list of tracked services
is made to get a definitive list of services that will actually be updated.

Each service gets updated individually and monitored for the amount of time
specified in the docker service configuration. If it fails to update and a
rollback is triggered, Docker will only roll back that service. deploy-webhook
rolls back all the other ones that have successfully updated up to that point.

The end result is that all services should be consistent at all times (except
during deploys) and there won't be scenarios where for example the main
application server runs one version of the code and your celery worker another.
