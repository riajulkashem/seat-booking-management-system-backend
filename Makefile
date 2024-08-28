# Variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PYTHON) manage.py

# Setup virtual environment and install dependencies
install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Run the Django development server
run:
	$(MANAGE) runserver

# Apply database migrations
migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

# Lint Python code and check coding standard
lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/black .
	$(VENV)/bin/mypy .
	$(VENV)/bin/isort .

# Run Django tests
test:
	$(MANAGE) test