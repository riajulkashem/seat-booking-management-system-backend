# Seat Booking Management System Backend

## Overview

The Seat Booking Management System Backend is a Django-based application. This README provides information on how to set up, run, and maintain the project.


## Requirements

- Python 3.12.5+
- Django 5.1+
- Django Rest Framework

## Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/riajulkashem/seat-booking-management-system-backend.git
cd seat-booking-management-system-backend
```

### 2. Create and Activate Virtual Environment
Use the Makefile to automate the setup:
```bash
make setup_project
```
Alternatively, manually set up the virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/data.json
```

### 3. Run the Development Server
Start the Django development server:
```
make run
````
Alternatively, run the server manually:
```bash
python manage.py runserver
```

### 4.Create a Test Superuser
Create a superuser with the username rk and password rk:
```
make createsuperuser
```
Alternatively, create a superuser manually:
```bash
python manage.py createsuperuser --username=rk --email=rk@mail.com --noinput
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='rk'); u.set_password('rk'); u.save()"
```

### 5. Access the Admin Panel
Open your browser and navigate to [admin/](http://localhost:8000/admin/) to access the Django admin panel. Log in using the superuser credentials created earlier.

### 6. Access the API Documentation
Open your browser and navigate to [api/docs/](http://localhost:8000/api/docs/) to access the API documentation.

### Linting and Code Quality
To ensure code quality, you can run the following linting commands:

```bash
make lint
```
Alternatively, manually run:
```bash
flake8 .
black .
mypy . --exclude 'migrations'
isort .
```

### Running Tests
To run the Django test suite:
```bash
make test
```
Alternatively, manually run:
```bash
python manage.py test
```
### Contributing
If you would like to contribute to the project, please fork the repository and submit a pull request with your changes. Ensure all tests pass and adhere to the project's coding standards.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

For further information, please refer to the [Django Documentation](https://docs.djangoproject.com/en/5.1/).