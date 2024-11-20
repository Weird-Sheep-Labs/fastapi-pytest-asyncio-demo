# fastapi-pytest-asyncio-demo

## Prerequisites

- Python 3.12+
- poetry
- Postgres

## Setup

- Install the project:

```
poetry install
```

- Create a local Postgres database. If you have `psql` installed you can simply run:

```
createdb <db_name>
```

- Create a `.env` file in the project root with the following:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/<db_name>
```

- Run the tests:

```
poetry run pytest
```
