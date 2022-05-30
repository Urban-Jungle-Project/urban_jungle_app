from app.api import bp
from flask import jsonify, request, url_for, abort

from app.api.constants import ResponseCodes, ErrorMessages
from app.models import Plant
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/plants/<int:id>', methods=['GET'])
@token_auth.login_required
def get_plant(id):
    return jsonify(Plant.query.get_or_404(id).to_dict())


@bp.route('/plants', methods=['GET'])
@token_auth.login_required
def get_plants():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Plant.to_collection_dict(Plant.query, page, per_page, 'api.get_plants')
    return jsonify(data)


@bp.route('/plants', methods=['POST'])
@token_auth.login_required
def create_plant():
    data = request.get_json() or {}
    for field in ['plant_name', 'user_id']:
        if field not in data:
            return bad_request(ErrorMessages.REQUIRED_PLANT_PARAMETERS.value)
    if token_auth.current_user().id != data['user_id']:
        return {"error": "403 Forbidden"}, ResponseCodes.FORBIDDEN.value
    if Plant.query.filter_by(plant_name=data['plant_name']).first():
        return bad_request(ResponseCodes.PLANT_EXISTS.value)
    plant = Plant()
    plant.from_dict(data)
    db.session.add(plant)
    db.session.commit()
    response = jsonify(plant.to_dict())
    response.status_code = ResponseCodes.SUCCESS.value
    response.headers['Location'] = url_for('api.get_plant', id=plant.id)
    return response


@bp.route('/plants/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.get_json() or {}
    if 'user_id' in data and token_auth.current_user().id != data['user_id']:
        return {"error": "403 Forbidden"}, ResponseCodes.FORBIDDEN.value
    if 'plant_name' in data and \
            Plant.query.filter_by(plant_name=data['plant_name']).first():
        return bad_request(ErrorMessages.PLANT_EXISTS.value)
    plant.from_dict(data)
    db.session.commit()
    return jsonify(plant.to_dict())


@bp.route('/plants/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    if token_auth.current_user().id != plant.user_id:
        return {"error": "403 Forbidden"}, ResponseCodes.FORBIDDEN.value
    db.session.delete(plant)
    db.session.commit()
    return '', ResponseCodes.NO_CONTENT.value
