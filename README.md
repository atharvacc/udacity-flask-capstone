# udacity-flask-capstone

## URL: https://movie-app-ac.herokuapp.com
## TOKENS PROVIDED IN postman collection, if unavailablke, please use the tokens provided in submiss

#Roles:
## Casting Assistant
- get:actors, get:movies
## Casting Director
- get:actors, get:movies, post:actors, delete:actors, patch:actors, patch:movies
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
## Executive Producer
- get:actors, get:movies, post:actors, delete:actors, patch:actors, patch:movies, post:movies, delete: movies

## Motivation
- to learn more about backend development

## dependencies 
- Python 3
- Flask
- Postgres
- SQLAlchemy
- Flask-SQL Alchemy
- psycopg2
- flask-migrate
- alembic 
- heroku 

##  Installation 
```
git clone  https://github.com/atharvacc/udacity-flask-capstone.git
cd udacity-flask-capstone
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Usage 
```
export FLASK_APP=app
export FLASK_DEBUG=True
flask run 
```

## unit tests 
```
python -m unittest
```

## API supported

### Get 
- /actors
- /movies 

### Delete
- /actors/\ `<id>`
- /movies/\ `<id>`

### POST
- /actors
- /movies

### PATCH
- /actors/\ `<id>`
- /movies/\ `<id>`