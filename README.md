# anwesenheitstool

## virtual environment
`python3 -m venv venv`

On Windows, run:
`venv\Scripts\activate.bat`\
falls das nicht geht, rufe vorher auf:
`Set-ExecutionPolicy Unrestricted -Scope Process`

On Unix or MacOS, run:
`source venv/bin/activate`

## Setup
`pip install -r requirements.txt`

## Useful commands

### Run local development server

```
python manage.py runserver
```

## Migration / Datenbank aktualisieren

```
python manage.py makemigrations meetup
python manage.py migrate -n 
```

### Debug Admin User / Superuser

Create: 
```
python manage.py createsuperuser
```
Falls von git bash aus:
```
winpty python manage.py createsuperuser
```

## Deploying

### Configuration
Copy `.env.template` to `.env`. Then add your configuration into the new `.env` file.

To check if your configuration is ready for deployment, run `docker-compose run django check --deploy` to do some automated checks.

Use Step 3 of the [Quick Start Guide](https://django-microsoft-auth.readthedocs.io/en/latest/usage.html#quickstart) of django-microsoft-auth to obtain your Microsoft related keys.

For generating the `DJANGO_SECRET_KEY`, use any password generator you like. The deployment check will complain if your key is too short, so make sure to run it!

### Docker-compose
Before doing `docker-compose up` make sure to run `docker-compose run django migrate` to initialize the database. 

The entrypoint pipes through its parameters to manage.py, so e.g. creating a superuser account using `docker-compose run django createsuperuser` is possible.

Also make sure to run `docker-compose build` or `docker-compose up --build` after making some changes
