## sanic_db

### Synopsis

    Sanic - Asynchronous Python - Postgresql - REST
    
### Usage

    git clone https://github.com/mprather1/sanic_db
    
    ./run.sh
    
### Routes

#### GET /models

    http http://<host>:<port>/models
    
#### GET /models/:id

    http http://<host>:<port>/models/<id>
    
#### POST /models

    http -f POST http://<host>:<port>/models name=<string> attribute=<integer>
    
#### PUT /models/:id

    http -f PUT http://<host>:<port>/models/<id> name=<string> attribute=<integer>
    
#### DELETE /models/:id

    http DELETE http://<host>:<port>/<id>