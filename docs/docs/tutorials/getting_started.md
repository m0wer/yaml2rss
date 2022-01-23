# Getting started

## Installation

```bash
make install
```

## Configuration

The following environment variables must be defined with the database
connection settings:

```bash
DB_NAME=''
DB_HOST=''
DB_USER=''
DB_PASS=''
DB_PORT=''
```

You can define them in several ways:

* passing them to `docker run` with the `-e VAR=value` argument.
* manually using `export`
* sourcing a script with the `export` commands
* saving them in your `virtualenv` `postactivate` script
* ...

## Running

### Development

For development, you can run the project with:

```bash
uvicorn yaml2rss.entrypoints.api.main:api --reload
```

You can then access the API at <http://localhost:8000> and the
[Swagger UI](https://swagger.io/tools/swagger-ui/)
(interactive API documentation) at <http://localhost:8000/docs>.

### Production

For production, a process manager is recommended to handle multiple
workers, such as `gunicorn`.

For example:

```bash
gunicorn \
    -b 0.0.0.0:8000 \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    yaml2rss.entrypoints.api.main:api
```

Options:

* `-b` option specifies the binding host and port.
* `-w` option specifies the number of workers.
* `-k` option specifies the type of workers, that need to be
  `uvicorn.workers.UvicornWorker` as specified at the
  [Uvicorn Documentation](https://www.uvicorn.org/deployment/).
