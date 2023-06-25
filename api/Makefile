.PHONY: setup collectstatic createsuperuser makemigrations merge-migrations dry-run-appmigrations app-migrations migrate lint-dev lint-apply

setup:
	@echo "Setting up and installing requirements...."
	python3 -m pip install --upgrade pip
	pip install virtualenv
	python3 -m venv env

collectstatic:
	@echo "Collecting static files ..."
	python3 manage.py collectstatic --no-input --clear

createsuperuser:
	@echo "Creating superuser...."
	python3 manage.py createsuperuser


makemigrations:
	@echo "Making migrations ..."
	python3 manage.py makemigrations

merge-migrations:
	@echo "Merging migrations ..."
	python3 manage.py makemigrations --merge

dry-run-appmigrations:
	@echo "checking for migrations to be made ..."
	python3 manage.py makemigrations ${APP} --check --dry-run

app-migrations:
	@echo "Making app migrations ..."
	python3 manage.py makemigrations ${APP}

migrate:
	@echo "Sync database and model changes ..."
	python3 manage.py migrate

lint-check:
	@echo "Checking for lint errors..."
	flake8 .
	black --check .
	isort --check-only .

lint-apply:
	@echo "apply linting ..."
	black .
	isort .

start-server:
	@echo "Starting Server..."
	python3 manage.py runserver ${PORT}

shell:
	@echo "Server Interractive shell..."
	python3 manage.py shell

shell_plus:
	@echo "Server Interractive shell..."
	python3 manage.py shell_plus


show_urls:
	@echo "Server Interractive shell..."
	python3 manage.py show_urls

startapp:
	@echo "Creating project application..."
	python3 manage.py startapp ${APP}

test-all:
	@echo "Running all tests together..."
	python3 manage.py test

test-class:
	@echo "Running testings for ${CLASS} ..."
	python3 manage.py test -k ${CLASS} --verbosity=2
