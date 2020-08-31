# Brasilprev Test

Brasilprev e-commerce simulation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements. Linux enviroments just follow the commands bellow:

```bash
$ git clone https://github.com/vandersondev/brasilprev.git
$ cd brasilprev
$ python3.8 -m venv env
$ source env/bin/activation
$ pip install -r requirements.txt
```

### Create SQLite Database:

```bash
$ python manage.py migrate
```

### Creating an admin user *
\* Only **admins are allowed to create products** in this application:

```bash
$ python manage.py createsuperuser
Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
Superuser created successfully.
```

## Usage

### Register an user

```bash
$ curl --location --request POST 'http://127.0.0.1:8000/api/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "<your username>",
    "password": "<your password>",
    "email": "<your email>"
}'
```

### Create a product:

1. Generate your base auth token

```bash
$ echo $(echo -n admin:123456 | base64 --wrap 0)
YWRtaW46MTIzNDU2

```

2. Take your token and replace in the header Authorization field.

```bash
$ curl --location --request POST 'http://127.0.0.1:8000/api/product/' \
--header 'Authorization: Basic <your auth token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "teste",
    "width": 30,
    "depth": 40,
    "height": 50,
    "weight": 100.0,
    "price": "150.90"
}'
```

**Remember, only superuser is allowed to add new products**

### Make a order

1. Generate your base auth token

```bash
$ echo $(echo -n vanderson:123456 | base64 --wrap 0)
dmFuZGVyc29uOjEyMzQ1Ng==
```

2. Take your token and replace in the header Authorization field.

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/order' \
--header 'Authorization: Basic <your auth token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "products": [
        {
            "product_id": 3,
            "product_quantity": 7
        },
        {
            "product_id": 2,
            "product_quantity": 8
        }
    ]
}'
```

## Tests

Inside the project folder run the flow command:

```bash
$ python manage.py test
```

## Docker build

First, change the database configuration to use a more scalable database like PostgreSQL in *brasilprev/settings.py*

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
After that, just run the build command:

```bash
$ docker build .
```

## To-Do list

- [x] User
- [x] Products
- [x] Orders

- [x] Auth
- [x] Dockerfile
- [x] Heroku Deploy