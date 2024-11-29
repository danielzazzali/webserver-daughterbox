from flask import Blueprint, jsonify, request

from config.config import get_env_variable
from models.network_model import get_ip_and_mask
from config.constants import ETHERNET_CONNECTION
from models.ethernet_model import set_ethernet_ip_and_mask

ethernet_bp = Blueprint('ethernet', __name__)


@ethernet_bp.route('/ethernet_ip_and_mask', methods=['GET'])
def get_ethernet_ip_and_mask_route():
    try:
        eth_connection_name = get_env_variable(ETHERNET_CONNECTION)
        data = get_ip_and_mask(eth_connection_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ethernet_bp.route('/set_ethernet_ip_and_mask', methods=['POST'])
def set_ethernet_ip_and_mask_route():
    try:
        ip = request.json.get('ip')
        mask = request.json.get('mask')

        if not ip or not mask:
            return jsonify({'error': 'IP address and mask are required'}), 400

        result = set_ethernet_ip_and_mask(ip, mask)
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500