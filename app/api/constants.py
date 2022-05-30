from enum import Enum


class ResponseCodes(int, Enum):
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    FORBIDDEN = 403


class ErrorMessages(str, Enum):
    REQUIRED_USER_PARAMETERS = 'User entry must include username, email and password fields.'
    REQUIRED_USER_PARAMETERS_PASSWORD_RULES = 'Password must be at least 8 characters.'
    REQUIRED_USER_PARAMETERS_USER_RULES = 'Username must be at least 1 character.'
    REQUIRED_USER_PARAMETERS_VALID_EMAIL_ADDRESS = 'Please use a valid email address.'
    USERNAME_EXISTS = 'Please use a different user name.'
    EMAIL_EXISTS = 'Please use a different email address.'
    PLANT_EXISTS = 'Please use a different plant_name.'
    REQUIRED_PLANT_PARAMETERS = 'Plant entry must include plant_name and user_id fields.'
