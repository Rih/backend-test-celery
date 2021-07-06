## cornershop-backend-test


### Complete env vars defined in env.example

### Copy env.example into .env in same folder
- `cp env.example .env`


### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

### After creating development environment

- run inside backend container: `sh bin/load-init.sh` 
