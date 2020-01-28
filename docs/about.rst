Overview
========

This project arose from a need to atomically update multiple Docker services.
A docker service update or stack deploy updates each service individually,
but what if two services depend on both having a specific version of the code
running? What if one updates and the other one fails and rolls back?

Deploy-webhook is a simple flask app which adresses that problem and adds
multiple other creature comforts for devs to interact with the application
stack while not having to ssh onto servers.

The app is still extremely experimental, WIP and mostly still hacked together.
The API is not stable and will most likely change until 1.0.0 and /api/v1 is
released. There is currently no ETA on that, but I do want to finish all the
items in the future plans section before that.

Finally, there is also a frontend application that's meant to be used with
this backend, but it's completely optional. Everything about it can be found
on its repo_.

.. _repo: https://github.com/TheEdgeOfRage/deploy-app

I encourage you to open issues and pull requests for any ideas and changes
you'd like to see. For any other questions you can contact me via email_.

.. _email: pavle.portic@tilda.center

Features
========

* Atomic stack updates
* Overview of active services
* Container management (logs and execs)

Future plans
============

* Cross-node container management
* Deploy endpoint security (HMAC signatures)
