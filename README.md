# GhibliWebApp
This simple web app gets data from https://ghibliapi.herokuapp.com/ and display it on `http://localhost:8000/movies` page.

## Getting started
The requirement to run this app is to install python 3, Django and pipenv in your OS.

install Django and Django rest framework and other libs in a virtual enviornment:

1. `cd /path/to/project/root/`
2. `pipenv install`

## Run the application
`python manage.py runserver`

## Run tests
`coverage run --source='api' manage.py test api`

## Get code coverage
`coverage report`
