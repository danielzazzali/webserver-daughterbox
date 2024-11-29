from flask import Blueprint, jsonify, request

from config.config import get_env_variable
from config.constants import WIRELESS_CONNECTION
from models.network_model import get_ip_and_mask
from models.wifi_model import remembered_wifi_connections, scan_wifi_networks, get_active_wifi_connection, \
    connect_to_new_ap, disconnect_from_wifi_connection, connect_to_known_wifi_connection, delete_known_wifi_connection, \
    set_autoconnect_on_to_wifi_connection, set_autoconnect_off_to_wifi_connection

wifi_bp = Blueprint('wifi', __name__)


@wifi_bp.route('/wifi_ip_and_mask', methods=['GET'])
def get_wifi_ip_and_mask_route():
    try:
        wifi_connection_name = get_env_variable(WIRELESS_CONNECTION)
        data = get_ip_and_mask(wifi_connection_name)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wifi_bp.route('/remembered_wifi_connections', methods=['GET'])
def get_remembered_wifi_connections_route():
    try:
        connections = remembered_wifi_connections()
        return jsonify({'connections': connections})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/scan_wifi_networks', methods=['GET'])
def scan_wifi_networks_route():
    try:
        networks = scan_wifi_networks()
        return jsonify({'networks': networks})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/active_wifi_network', methods=['GET'])
def get_active_wifi_connection_route():
    try:
        network = get_active_wifi_connection()
        return jsonify({'network': network})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/connect_to_new_ap', methods=['POST'])
def connect_to_new_ap_route():
    try:
        ssid = request.json.get('ssid')
        password = request.json.get('password')

        if not ssid or not password:
            return jsonify({'error': 'SSID and password are required'}), 400

        result = connect_to_new_ap(ssid, password)
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/disconnect_from_wifi_connection', methods=['POST'])
def disconnect_from_wifi_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        disconnect_from_wifi_connection(connection_name)
        return jsonify({'message': f"Disconnected from network '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/connect_to_known_wifi_connection', methods=['POST'])
def connect_to_known_wifi_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        connect_to_known_wifi_connection(connection_name)
        return jsonify({'message': f"Connected to network '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/delete_known_wifi_connection', methods=['POST'])
def delete_known_wifi_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        delete_known_wifi_connection(connection_name)
        return jsonify({'message': f"Connection '{connection_name}' deleted successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/set_autoconnect_on_to_wifi_connection', methods=['POST'])
def set_autoconnect_on_to_wifi_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        set_autoconnect_on_to_wifi_connection(connection_name)
        return jsonify({'message': f"Autoconnect set to 'yes' for connection '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@wifi_bp.route('/set_autoconnect_off_to_wifi_connection', methods=['POST'])
def set_autoconnect_off_to_wifi_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        set_autoconnect_off_to_wifi_connection(connection_name)
        return jsonify({'message': f"Autoconnect set to 'no' for connection '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500





