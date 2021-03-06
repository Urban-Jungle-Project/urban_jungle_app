from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from app.api.constants import ResponseCodes


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(ResponseCodes.BAD_REQUEST.value, message)

