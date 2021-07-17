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

user: `admin-v`, `admin-k`

mail: `***REMOVED***`, `***REMOVED***`

password: `summerofcode`, `summerofcode`

## Deploying

Before doing `docker-compose up` make sure to run `docker-compose run django migrate` to initialize the database. 

The entrypoint pipes through its parameters to manage.py, so e.g. creating a superuser account using `docker-compose run django createsuperuser` is possible.

Also make sure to run `docker-compose build` or `docker-compose up --build` after making some changes