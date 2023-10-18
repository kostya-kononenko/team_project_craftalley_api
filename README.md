# Craftalley API

## Installation
#### Install Python 3:
- Please checkout https://realpython.com/installing-python/

#### Create virtual environment:
- Go to you project directory, then
```shell
> python3 -m venv env
```
```shell
> source env/bin/activate
```

#### Install requirements:
```shell
> pip install -r requirements.txt
```

#### Make migrations:

```shell
> python manage.py makemigrations
```

```shell
> python manage.py migrate
```

## Create super user
```shell
> python manage.py createsuperuser
```

## Create fixture for fake user, product, catalog, category use:

```shell
> python manage.py create_fixture.py
```


## Running API Server
```shell
> python manage.py runserver
```

## Generate your token
http://127.0.0.1:8000/user/token/


## All endpoint

http://127.0.0.1:8000/doc/swagger/

or

http://127.0.0.1:8000/doc/redoc/
