# Impiricus Project

## Requirements

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.
* Vite, React, lucide-react for frontend

## Start

Start the local development environment with Docker Compose. Use docker-compose up --build the first time to build images. Then you can just use docker-compose up

To start local frontend you must install lucide using "npm install lucide-react". Then run as normal using "npm run dev".

## General Workflow

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ uv sync
```

Then you can activate the virtual environment with:

```console
$ source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

## Backend tests

To test the backend run:

```console
$ bash ./backend/unittest.sh
```

The tests run with Pytest

### Test running stack

If your stack is already up and you just want to run the tests, you can use:

```bash
docker compose exec backend bash unittest.sh
```

That `/app/scripts/tests-start.sh` script just calls `pytest` after making sure that the rest of the stack is running. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker compose exec backend bash unittest.sh -x
```
### Development URLs

Development URLs, for local development.

Frontend: http://localhost:5173

Backend: http://localhost:8000

Automatic Interactive Docs (Swagger UI): http://localhost:8000/docs
