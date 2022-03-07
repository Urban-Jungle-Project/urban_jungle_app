# Urban Jungle Application Overview

Urban Jungle application provides ability to care for your home plants. 

# API documentation

## User APIs

| HTTP Method | Resource URL| Notes | 
| ---  | --- | ---|
| GET  | /api/users/\<id> | Return a user. |
| GET  | /api/users       | Return the collection of all user. |
| POST | /api/users       | Register a new user account. |
| PUT  | /api/users       | Return the collection of all users. |


## API Authentication

To receive an auth token please send request with basic authentication credentials:
~~~
http --auth <username>:<password> POST http://localhost:5000/api/tokens
~~~

For authentication of API request send "bearer" token using Authorization header. 
~~~
http GET http://localhost:5000/api/users/<id> "Authorization:Bearer <token>"
~~~










