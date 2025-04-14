from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
import subprocess

services = Blueprint('services', __name__)

@services.route('/', methods=['GET'])
@jwt_required()
def list_services():
    try:
        result = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--no-pager'],
            capture_output=True,
            text=True
        )
        return jsonify({"services": result.stdout.splitlines()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@services.route('/<string:service_name>', methods=['POST'])
@jwt_required()
@admin_required
def manage_service(service_name):
    action = request.json.get('action')
    valid_actions = ['start', 'stop', 'restart', 'status']
    
    if action not in valid_actions:
        return jsonify({"error": "Action non valide"}), 400
    
    try:
        result = subprocess.run(
            ['systemctl', action, service_name],
            capture_output=True,
            text=True
        )
        return jsonify({
            "service": service_name,
            "action": action,
            "output": result.stdout,
            "error": result.stderr
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500