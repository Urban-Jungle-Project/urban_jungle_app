# Urban Jungle Application Overview

Urban Jungle application provides ability to care for your home plants. 

# API endpoints

| Endpoint | Details|  
| ---  | --- |
| /tokens | **Obtain bearer token [POST]**:<br/>curl -u "\<username>:\<password>" -X POST http://\<host\>:\<port\>/api/tokens <br/> <hr/>Not Allowed - OPTIONS, HEAD, GET, PUT, PATCH, DELETE, TRACE |
| /users | **Get a collection of users [GET]**:<br/>curl -H "Authorization: Bearer \<token>" http://\<host\>:\<port\>/api/users <br/><br/> **Sign up new user [POST]**:<br/>curl -X POST -H "Content-Type: application/json" -d '{"email":"test@example.com","username":"example user","password":"12345678"}' http://\<host\>:\<port\>/api/users<br/> <hr/>Not Allowed - OPTIONS, HEAD, PUT, PATCH, DELETE, TRACE |
| /users/{uuid} | **Get user by id [GET]**:<br/>curl -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" http://\<host\>:\<port\>/api/users/1<br/><br/> **Update user by id [PUT]**:<br/>curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" -d '{"email":"test@example.com","username":"example user","password":"12345678"}' http://\<host\>:\<port\>/api/users/1<br/> <hr/>Not Allowed - OPTIONS, HEAD, POST, PATCH, DELETE, TRACE |
| /plants | **Get a collection of plants [GET]**:<br/>curl -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" http://\<host\>:\<port\>/api/plants <br/><br/> **Create new plant [POST]**:<br/>curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" -d '{"plant_name":"example name", "user_id": 1}' http://\<host\>:\<port\>/api/plants<br/> <hr/>Not Allowed - OPTIONS, HEAD, PUT, PATCH, DELETE, TRACE |
| /plants/{uuid} | **Get plant by id [GET]**:<br/>curl -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" http://\<host\>:\<port\>/api/plants/1<br/><br/> **Update plant by id [PUT]**:<br/>curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" -d '{"plant_name":"example name changed", "user_id": 1}' http://\<host\>:\<port\>/api/users/1<br/><br/> **Delete plant by id [DELETE]**:<br/>curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer \<token>" http://\<host\>:\<port\>/api/plants/1<br/> <hr/>Not Allowed - OPTIONS, HEAD, POST, PATCH, TRACE |











