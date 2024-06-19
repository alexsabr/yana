# YANA : Yet Another News Aggregator


The Goal of this project is to create a small django-based website to allow visitors to notice  differences in media reporting real world events. Currently centered on french media only.


### Building the project

Building the project requires Docker and make.

Configure the environment of the containers by modifying the file located at ``docker/.env``.

Run `make dock` to create the docker image of the project 
Run `make run-compose` to launch all the containers of the yana project
(Currently Database and Backend)


