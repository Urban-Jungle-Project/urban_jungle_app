from app.api import bp
from flask import jsonify, request, url_for

from app.api.constants import ErrorMessages, ResponseCodes
from app.models import User
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth
from email_validator import validate_email, EmailNotValidError


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    for field in ['username', 'email', 'password']:
        if field not in data:
            return bad_request(str(ErrorMessages.REQUIRED_USER_PARAMETERS.value))
    if User.query.filter_by(username=data['username']).first():
        return bad_request(ErrorMessages.USERNAME_EXISTS.value)
    if User.query.filter_by(email=data['email']).first():
        return bad_request(ErrorMessages.EMAIL_EXISTS.value)
    if len(data['password']) < 8:
        return bad_request(ErrorMessages.REQUIRED_USER_PARAMETERS_PASSWORD_RULES.value)
    if len(data['username']) < 1:
        return bad_request(ErrorMessages.REQUIRED_USER_PARAMETERS_USER_RULES.value)
    try:
        validate_email(data['email']).email
    except EmailNotValidError:
        return bad_request(ErrorMessages.REQUIRED_USER_PARAMETERS_VALID_EMAIL_ADDRESS.value)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = ResponseCodes.CREATED.value
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        return {"error": "403 Forbidden"}, ResponseCodes.FORBIDDEN.value
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request(ErrorMessages.USERNAME_EXISTS.value)
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request(ErrorMessages.EMAIL_EXISTS.value)
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())