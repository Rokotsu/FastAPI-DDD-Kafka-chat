# FastAPI + Kafka DDD chat Application w\ MongoDB

This is a basic template for FastAPI chat projects configured to use Docker Compose, Makefile, and a Vite + React frontend.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. Install all required packages in `Requirements` section.


### Implemented Commands

* `make app` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make app-down` - down application and all infrastructure
* `make app-shell` - go to contenerized interactive shell (bash)
* `make frontend` - run Vite + React frontend

### Most Used Django Specific Commands

* `make migrations` - make migrations to models
* `make migrate` - apply all made migrations
* `make collectstatic` - collect static
* `make superuser` - create admin user

## Frontend

The frontend lives in `frontend/` and proxies API calls to the FastAPI container.

### Run frontend with Docker

1. Start the backend:

   ```bash
   make app
   ```

2. Start the frontend:

   ```bash
   make frontend
   ```

3. Open the UI at [http://localhost:5173](http://localhost:5173) and submit a chat title.
