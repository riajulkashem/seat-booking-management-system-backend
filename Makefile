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
	$(MANAGE) migrate

# Create new migrations based on model changes
makemigrations:
	$(MANAGE) makemigrations

# Create a superuser
createsuperuser:
	$(MANAGE) createsuperuser

# Run Django tests
test:
	$(MANAGE) test

# Lint Python code using flake8
lint:
	$(VENV)/bin/flake8 .

# Format Python code using black
format:
	$(VENV)/bin/black .
	$(VENV)/bin/isort .

# Type check Python code using mypy
typecheck:
	$(VENV)/bin/mypy .

# Run all linting and formatting checks
check: lint format typecheck

# Clean up byte-compiled files
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

# Clean up virtual environment
clean-venv:
	rm -rf $(VENV)

# Build and run the project from scratch
build: clean clean-venv install migrate run
