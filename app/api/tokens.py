from flask import jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.constants import ResponseCodes


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    expires_in = 20
    token = basic_auth.current_user().get_token(expires_in=expires_in)
    db.session.commit()
    return jsonify({'access_token': token, 'token_type': 'Bearer', "expires_in": expires_in})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', ResponseCodes.NO_CONTENT.value
