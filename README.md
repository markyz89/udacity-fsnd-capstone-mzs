# Udacity Full Stack Nanodegree Capstone Project

## Introduction

This capstone project brings together all elements of the Udacity Full-Stack Nanodegree programme in one application. This is a backend API complete with testing and authentication, deployed on a cloud server.

The project is a Film API, comprising of actors and movies. The API is not publicly accessible, it is only available for users with an access token.

Casting assistants are able to view movies and actors.

Casting directors can view and modify movies and actors, and also have the ability to delete actors, but not movies.

Executive producers are all-powerful, having the ability to view, modify or delete both actors and movies.

## Installation

The project is running at https://udacity-fsnd-capstone-mzs.herokuapp.com/

It was built in an environment with Python 3.8.10 but is running on Heroku on Python 3.9.7.

To install locally, install python3 and pip.  To install the other requirements associated with this project:

```
pip install -r requirements.txt
```

Run the server with:
```
flask run
```

Authentiction tokens are provided within the auth_details.py file. You will require these in your authorisation headers in order to access any of the endpoints.

This project uses an SQLite database for simplicity which is included in the repo.

The app will be hosted by default at http://127.0.0.1:5000/ locally.

## API Reference

### Errors

Errors are returned as JSON objects in the following format:

```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return four error types when requests fail:

* 400 Bad Request
* 403 Forbidden
* 404 Resource Not Found
* 405 Not Allowed
* 422 Unprocessable

### Resource Endpoint Library

#### GET Actors

* General
   - Returns the list of actors as an object and a success value.
* Sample: ```curl https://udacity-fsnd-capstone-mzs.herokuapp.com/actors \
--header 'Authorization: Bearer {token} \```

```
{
    "actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 1,
            "name": "Leonardo Di Caprio"
        },
        ...
        {
            "age": 58,
            "gender": "male",
            "id": 3,
            "name": "Tonya Hanks"
        }
    ],
    "success": true
}
```


#### POST Actors
* General
  - Returns the id of the created actor and a success value.

Sample request:
```
curl --location --request POST 'https://udacity-fsnd-capstone-mzs.herokuapp.com/actors' \
--header 'Authorization: Bearer {token} \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Brad Pitt",
    "age": "47",
    "gender": "male"
}'
```

Returned value:
```
{"created":4,"success":true}
```


#### DELETE Actors
* General
   - Deletes an actor from the database
   - Returns a success value, the id of the deleted actor and the total number of actors remaining in the database.

Sample request:

 ```
curl --location --request DELETE 'https://udacity-fsnd-capstone-mzs.herokuapp.com/actors/3' \
--header 'Authorization: Bearer {token}'
```

Returned value:
```{
    "deleted": 4,
    "success": true,
    "total_actors": 3
}
```


#### PATCH Actors
* General
   - Changes some of the values of an actor from the database
   - Returns a success value, and the actor object.

Sample Request:
```curl --location --request PATCH 'https://udacity-fsnd-capstone-mzs.herokuapp.com/actors/4' \
--header 'Authorization: Bearer {token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Elliot Page",
    "age": 25,
    "gender": "male"
}'
```

Return Value:
```
{
    "actor": {
        "age": 25,
        "gender": "male",
        "name": "Elliot Page"
    },
    "success": true
}
```

#### GET Movies

* General
   - Returns the list of movies as an object and a success value.
* Sample: ```curl https://udacity-fsnd-capstone-mzs.herokuapp.com/movies \
--header 'Authorization: Bearer {token} \```

```
{
    "movies": [
        {
            "id": 1,
            "release_date": 2010,
            "title": "Inception"
        },
        ...
        {
            "id": 4,
            "release_date": 2004,
            "title": "Shaun of the Dead"
        }
    ],
    "success": true
}
```


#### POST Movies
* General
  - Returns the id of the created movie and a success value.

Sample request:
```
curl --location --request POST 'https://udacity-fsnd-capstone-mzs.herokuapp.com/movies' \
--header 'Authorization: Bearer {token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Dawn of the Dead",
    "release_date": 1999
}''
```

Returned value:
```
{"created":5,"success":true}
```


#### DELETE Movies
* General
   - Deletes an movie from the database
   - Returns a success value, the id of the deleted movie and the total number of movies remaining in the database.

Sample request:

 ```
curl --location --request DELETE 'https://udacity-fsnd-capstone-mzs.herokuapp.com/actors/3' \
--header 'Authorization: Bearer {token}'
```

Returned value:
```{
    "deleted": 4,
    "success": true,
    "total_movies": 3
}
```


#### PATCH Movies
* General
   - Changes some of the values of a movie from the database
   - Returns a success value, and the movie object.

Sample Request:
```
curl --location --request PATCH 'http://127.0.0.1:5000/movies/4' \
--header 'Authorization: Bearer {token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Shaun of the Dead",
    "release_date": 2004
}'
```

Return Value:
```
{
    "movie": {
        "title": "Shaun of the Dead",
        "release_date": 2004
    },
    "success": true
}
```

## Authors
Starter code provided by Udacity, all other code authored by Mark Simpson.
