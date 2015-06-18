## Load Balancer Example (Docker Compose) 

First, [install Docker Compose](https://docs.docker.com/compose/install/)

```
$ docker-compose up
$ curl http://localhost:5000 # test endpoint
...
$ docker-compose scale web=3 # upscale
$ curl http://localhost:5000
...
$ docker-compose scale web=1 # downscale
$ curl http://localhost:5000
...
```