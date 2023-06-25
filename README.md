# Data-Exchange-Platform

This is the backend code for the Data Exchange Platform code

## Getting Started

These instructions will cover how to setup, run and test the api

### Prerequisities

In order to run this code you will need

* [Python3 Installed](https://realpython.com/installing-python/)
* [venv installed](https://docs.python.org/3/library/venv.html)

#### How to setup the project

Clone project and change directory to project folder. 

```sh
git clone https://github.com/patrickcmdtelnet/Data-Exchange-Platform.git
cd Data-Exchange-Platform
git fetch --all
```

Type the commands below to successfully setup the project on your machine

```sh
python3 -m pip install --upgrade pip
pip install virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

For the rest of the instructions below make sure you are in the `api` directory. For more information see [TEST API](https://github.com/patrickcmdtelnet/Data-Exchange-Platform/blob/main/README.md#testing-the-api) section.

```sh
cd api
```

Run database migrations

```sh
make migrate
```

Create application superuser. Follow the prompts from the command below

```sh
make createsuperuser
```

Then start the server. Make sure to replace `<port_number>` with the appropriate port number e.g `8000`, `8001` etc

```sh
make start-server PORT=<port_number>
```

### Other userful commands

Activate virtual environment

```sh
source env/bin/activate
```

Start new project application

```sh
make startapp APP=<app_name>
```

If you create new or make changes to database models, you can run migration dry runs to see what changes will be effected

```sh
make dry-run-appmigrations APP=<app_name>
```

Make database migrations and migrate

```sh
make app-migrations APP=<app_name>
make migrate
```

Collect static files

```sh
make collectstatic
```

Check for linting errors

```sh
make lint-check
```

Apply linting

```sh
make lint-apply
```

### Testing the API

Checkout steps [here](./API_TEST.md)
