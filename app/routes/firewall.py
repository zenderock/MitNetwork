from flask import Blueprint, request, jsonify
from app.services.firewall import (
    get_firewall_rules,
    add_firewall_rule,
    delete_firewall_rule
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import admin_required

firewall = Blueprint('firewall', __name__)

@firewall.route('/', methods=['GET'])
@jwt_required()
def get_rules():
    try:
        rules = get_firewall_rules()
        return jsonify(rules), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@firewall.route('/', methods=['POST'])
@jwt_required()
@admin_required
def add_rule():
    data = request.get_json()
    try:
        result = add_firewall_rule(
            protocol=data.get('protocol'),
            port=data.get('port'),
            action=data.get('action', 'ACCEPT'),
            source=data.get('source', '0.0.0.0/0')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@firewall.route('/<int:rule_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def remove_rule(rule_id):
    try:
        result = delete_firewall_rule(str(rule_id))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400