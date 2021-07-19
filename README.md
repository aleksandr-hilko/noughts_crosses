# README #

### Summary ###

Dockerized app that represents naughts and crossses game that is written in Python using Flask framework and uses MongoDB as backend.

### Stack ###

1. Python
2. Flask
3. MongoDB (flask_pymongo as client library)
4. Docker
5. Nginx
6. Gunicorn

### Run ###

To run the project locally, you need to execute the following:

``
docker-compose up --build 
``

This will build and start the project locally.

*Important note*: the project is using nginx and uses 80 port, so please make sure that it is opened on your local station.


### How to test ###

---coming soon----

### API desctiption ###

1. To start using app you should register with

    **POST auth/register** and provide following information in the request body: 
```
{
	"first_name": "Alex",
	"last_name": "Test",
	"email": "test@test.com",
	"password": "12344"
}
```

JWT Authentication / Authorization is used in the app and all api endpoints expect existence of jwt token in Authorization header.

2. So upon successful registration you should login with your email and password:

    **POST auth/login** and provide following information in the request body:
``` 
{
	"email": "test@test.com",
	"password": "12344"
} 
```

On successful responce you should receive access_token that should be further used to authorize in the app. Please don't
forget to add authorization header in format Authorization: Bearer {access_token} on further requests to the app.

3. To start a game you should use

    **POST games/** and provide following information in the request body: 
```
{
	"board_size": int,
	"line_len_to_win": int
}
```
where line_len_to_win - is the number of points in a line for a user which determines victory in a game, it should be less then 
board_size. Id of a newly created game should be returned in the response.

4. To make a move please use

    **POST games/<str:game_id>/move** and provide following information in the request body: 

```
{
	"x": 4,
	"y": 2
},
```

where x,y - coordinates that you want move on. 

In the response you should receive your move, computer move and status of a game.

5. To inspect list of your games along with some statistics please use 

    **GET games/**
