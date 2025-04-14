from flask import Blueprint, jsonify
from app.services.monitoring import (
    get_network_usage,
    get_active_connections,
    get_system_stats
)
from flask_jwt_extended import jwt_required

monitoring = Blueprint('monitoring', __name__)

@monitoring.route('/network', methods=['GET'])
@jwt_required()
def network_stats():
    try:
        stats = get_network_usage()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitoring.route('/connections', methods=['GET'])
@jwt_required()
def active_connections():
    try:
        connections = get_active_connections()
        return jsonify(connections), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitoring.route('/system', methods=['GET'])
@jwt_required()
def system_stats():
    try:
        stats = get_system_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500