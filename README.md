# Beets DB Web API

Web API for the [beets](http://beets.io) database.

This API does not use beets's data model and operates on the SQLite database directly. Although this is not very elegant and generally rather objectionable, this route has been chosen because of its performance and simplicity advantages, thereby making the beets data accessible even to systems that have relatively low performance, such as the Raspberry Pi.

Furthermore it should be noted that this API is created merely as a means to enable building a web-based application for managing album genres. That project can be found [here](https://github.com/bartkl/beets-genremanager). It will therefore be minimal and one should not expect too much maintenance or maturity of the project, since there are no intentions to extend its purpose beyond this scope.


## GraphQL
GraphQL is used as a query language for communicating between the frontend and
the bagend. Possibly the frontend is going to use Apolle as their main
provider.

For the backend, setting up [graphene-python](https://docs.graphene-python.org/en/latest/quickstart/) would be nice.
