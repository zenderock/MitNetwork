from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required
import subprocess

logs = Blueprint('logs', __name__)

@logs.route('/system', methods=['GET'])
@jwt_required()
@admin_required
def system_logs():
    try:
        result = subprocess.run(
            ['journalctl', '-n', '100', '--no-pager'],
            capture_output=True,
            text=True
        )
        return jsonify({"logs": result.stdout.splitlines()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logs.route('/auth', methods=['GET'])
@jwt_required()
@admin_required
def auth_logs():
    try:
        result = subprocess.run(
            ['tail', '-n', '100', '/var/log/auth.log'],
            capture_output=True,
            text=True
        )
        return jsonify({"logs": result.stdout.splitlines()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500