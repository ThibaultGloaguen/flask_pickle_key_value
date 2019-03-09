# Key value application

This application is written in python 2.7  and uses the Flask framework and PickleDB.
It was developed and tested on macOS High Sierra distribution.
It allow you to store, get and delete key value objects throught an http API.

| Method | Path | README |
| ------ | ------ | ------ |
| GET | /keys/{id} | get a value  |
| GET | /keys | get all values ( optional parameter: filter, support wildcards. Example: filter=wo$d gives you => world, wod, word, etc .. ) |
| HEAD | /keys/{id} | check if value exists |
| DELETE | /keys/{id} | delete value |
| PUT | /keys | set a value ( optional parameter: expire_in, set an expiracy time `in seconds` when adding a value) |
| DELETE | /keys | delete all values |

The client should send data in json format with the following header : `Content-Type: application/json`


# Installation

This application requires Docker to run.
By default, the Docker will expose port 8000. To change this configuration, you can modify the docker-compose.yml to choose another port.
To install and run the server application:
```sh
$ docker-compose build
```

# Run
```sh
$ docker-compose up application
```
The server should now run on http://0.0.0.0:8000

### Tests

This solution is provided with local tests and integration tests.
To run those tests:
```sh
$ docker-compose up test
```

### Architecture
The entry point of the application is the run.py file. This is where the Flask server application is launched
The application is separated in 4 directories
* /models
* /routes
* /services
* /metrics

**Routes**

The routes directory contains 1 file: keys_route.py. This part of the application handles all the http requests from the client and route them to the right service.
It also handles the differents errors that the application can throws such as Not Found Error, Expired Error, Bad Request of Internal Error

**Services**

The services directory contains 2 files: database_service.py and key_store_service.py.
The database_service deals with all the database access.

The key_store_service is the interface between the client and the database. It handle operations on the database and assure that the data is reliable when it is saved or requested.
The service inherits from database_service, in this case it can use all the accessing methods to the database.

**Models**

the model directory contains the key_store_model.py file which is the representation of the value object in database.

The data model has 1 method:
- `to_dict()` : this method iterates over every attributes of the class and transform our class Object into a serializable dictionary. this method is used when the object is saved in DB

**metrics**

The metrics directory contains 1 file: metrics_handler.py. This file set the flask application in the method `setup_metric` so that it can counts the number of entrance requests and the response latency.

### Prometheus

This application is instrumented and can provides some metrics to the prometheus interface.
It is possible to check for :
- the number total of request with the name `request_count`
- the server response latency for each requests with the name `request_latency_seconds`
- the number total of internals errors and the error label for every errors with the name `internal_error_count`


### Remarks

Concerning the PUT method on request path /keys, there are multiple points to discuss.
* The challenge documentation didn't mentioned about saving multiples values with this endpoint.
But if the client send more than one key/value in the json payload on this endpoint, I decided to insert them all in DB in one API call.
* If the client decides to PUT one key/value pair but  the same key is already stored in DB.
I had two choices here: 1. Throw an exception to inform the client that this key is already present in the database and not save it. 2. Erase the old value associated to the key in database with the new one sended by the client

I choose solution 2, but both are possible in this implementation.

#### Limitations

If this solution has to deal with a large amount of data, some problems could happens such as:
 *  as the Docker image is hosting the database file, the bigger the data stored will be the bigger the docker image will be, there could be a memory problem for the docker image host if we talk about very large amount of data.
 *  The endpoint /keys to get all values could take a lot of time to respond if the application have to retrieve all the datas.

### Optimizations && enhancement

To deals with the large amount of data problem, some optimizations can be done such as:
* Not to host the database on the docker image but separates the database in another docker image that could be hosted in the cloud provider. The problem with this solution is that the solution requires a internet connection to work and secured authentication to access the online database.
* For the get all problem, the solution could provides a pagination system to send a limited amount of data per request and not to get an enormous amount of data in one shot.

The solution could also provides a endpoint to update a value in DB. To follow the REST standart it could be the endpoint /key/{id} with the method PATCH.



Thanks for reading ;)