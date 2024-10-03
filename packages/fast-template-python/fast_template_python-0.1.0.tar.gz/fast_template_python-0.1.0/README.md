## Fast Template

Easily generate a template for your [FastAPI](http://fastapi.tiangolo.com) applications, complete with JWT authentication and Google sign-in.

### Installation

You can install Fast Template via `pip`:

```sh
pip install fast_template
```

Or using `poetry`:

```sh
poetry add fast_template
```

### Usage

To initialize a project in an existing folder:

```sh
fast-template init project_name .
```

To create a new project:

```sh
fast-template init project_name
```

Once the template is set up, you'll need to create a `.env` file as required by the `settings.py` file (feel free to modify it to suit your needs).

#### Migrations

You can set up database migrations using Alembic:

```sh
alembic init migrations
```

For more information on using Alembic, check the [official tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html#creating-an-environment).

### Features

#### Authentication
- JWT-based authentication is built-in.
- Google sign-in is fully integrated, right down to the database layer.

#### Extensible Folder Structure
The folder structure is designed to be modular and scalable, inspired by Philip Okiokio ([LinkedIn](https://www.linkedin.com/in/philip-okiokio/), [GitHub](https://github.com/philipokiokio)). It promotes loose coupling and clean separation of concerns.

Each operation is handled by three main layers:
1. **Router Layer**: Defines FastAPI routes.
2. **Service Layer**: Contains the business logic.
3. **Database Layer**: Manages database interactions.

The data flow is structured as follows:

```
Router Layer → Service Layer → Database Layer
```

The service layer handles the data exchange between the router and the database, while the router serializes requests and passes them to the service.

#### Pre-configured Services
The root folder contains core services required for the backend, including:
1. Database setup
2. Redis caching
3. Email templates
4. Background workers (using ARQ)
5. Logging configuration
6. Application settings

#### Schema and Database Layers
- **Schema**: Pydantic models for serialization/deserialization, organized by feature (e.g., authentication schemas are in the `auth` folder).
- **Database**: Handlers and ORM integration using [SQLAlchemy](http://sqlalchemy.org).

### Work in Progress
This package is a work in progress, created to streamline the setup of backend projects.

### 🐛 Bugs/Feature Requests

Contributions are welcome! Feel free to open a pull request or an issue for feature requests or bug reports.
