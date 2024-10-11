# IoT Smart Home -- CMP6207 

This work was carried out for the module CMP6270 - Modern Data Stores, as part of my undergraduate degree in Computer and Data Science.

## About 

The focus is on the IoT data that will be used within a smarthome and how it can be modelled and stored within MongoDB, along with the configuration of MongoDB itself. To show proof of concept, an API and front-end were creted to view the data within the MongoDB database. 

Some features include: 
 - Replication via MongoDB Replica Set
 - RESTful API
 - Front-end 

## Running the project 

### Starting MongoDB and the RESTFul API 

The way the project has been run is to start up Docker via a devcontainer in VS Code from the /backend directory. This will in turn run the Docker Compose file. If you are not doing it this way you can run `docker compose up` from the root directory of the project, however, if you are running the init_db script locally, the connection string will need to be modified. 

Once the containers are running, the replica set needs to be initialised, this can be done by running  `docker exec -it <container_name> mongosh` (where container_name is the name of any of the MongoDB instances), this is followed by the following inside mongosh, `use admin`, `db.auth("admin", "secret")`, now the replica set can be initialised with `rs.initiate({_id:'rs0',members:[{_id:0,host:'host.docker.internal:27017',priority:1},{_id:1,host:'host.docker.internal:27018',priority:0.5},{_id:2,host:'host.docker.internal:27019',priority:0.5}]})`

Next initialise the database using the init_db.py script. 

The database is now fully operational including replication and dummy data. 

### Starting the front-end 

Inside the frontend directory run `npm install react-scripts` & `npm start`

## Disclaimer

The assignment is focused on MongoDB and more widely NoSQL databases and their uses. The source code is as it was for assignment purposes, which leads to credentials (fake) being published, and a less-than-optimal experience setting up the project from scratch. 
