# django-todolist-api
A sample todo list built using Django/Django REST Framework API and developed in TDD using pytest

# Installation
Create a new python virtual environment <br/>
- run `python3 -m venv venv` <br/>

Install the dependencies from 'requirements.txt'<br/>
- In the root directory, run `pip install -r requirements.txt` <br/>

Then you're all set!

# Running the server
Make sure all migrations are migrated <br/>
- run `python manage.py makemigrations`
- run `python manage.py migrate`

To run the application locally, <br/>
- run `python manage.py runserver`
- open a browser to `http://127.0.0.1:8000/` or `http://localhost:8000/`

### Current active routes:
- `/admin`

# Run tests
- run `pytest`
