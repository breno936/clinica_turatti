from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping')
def ping():
    return {"message": "pong"}
