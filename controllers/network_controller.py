from flask import Blueprint, jsonify, request
from models.network_model import get_ip_and_mask, remembered_connections, scan_wifi_networks, get_active_wifi_network, \
    delete_connection, connect_to_known_network, disconnect_from_network, set_autoconnect_off, set_autoconnect_on, \
    get_eth_ip_and_mask, set_eth_ip_and_mask, connect_to_new_ap

network_bp = Blueprint('network', __name__)


@network_bp.route('/ip', methods=['GET'])
def get_ip():
    try:
        data = get_ip_and_mask()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@network_bp.route('/remembered_connections', methods=['GET'])
def get_remembered_connections():
    try:
        connections = remembered_connections()
        return jsonify({'connections': connections})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/scan_wifi_networks', methods=['GET'])
def get_scan_wifi_networks():
    try:
        networks = scan_wifi_networks()
        return jsonify({'networks': networks})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/active_wifi_network', methods=['GET'])
def get_active_wifi_network_route():
    try:
        network = get_active_wifi_network()
        return jsonify({'network': network})
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/delete_connection', methods=['POST'])
def delete_connection_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        delete_connection(connection_name)
        return jsonify({'message': f"Connection '{connection_name}' deleted successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/connect_to_network', methods=['POST'])
def connect_to_network_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        connect_to_known_network(connection_name)
        return jsonify({'message': f"Connected to network '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/disconnect_from_network', methods=['POST'])
def disconnect_from_network_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        disconnect_from_network(connection_name)
        return jsonify({'message': f"Disconnected from network '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/set_autoconnect_off', methods=['POST'])
def set_autoconnect_off_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        set_autoconnect_off(connection_name)
        return jsonify({'message': f"Autoconnect set to 'no' for connection '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/set_autoconnect_on', methods=['POST'])
def set_autoconnect_on_route():
    try:
        connection_name = request.json.get('connection_name')
        if not connection_name:
            return jsonify({'error': 'Connection name is required'}), 400
        set_autoconnect_on(connection_name)
        return jsonify({'message': f"Autoconnect set to 'yes' for connection '{connection_name}' successfully."}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/eth_ip', methods=['GET'])
def get_eth_ip_route():
    try:
        data = get_eth_ip_and_mask()
        return jsonify(data), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@network_bp.route('/set_ip', methods=['POST'])
def set_ip_route():
    try:
        ip = request.json.get('ip')
        mask = request.json.get('mask')

        if not ip or not mask:
            return jsonify({'error': 'IP address and mask are required'}), 400

        result = set_eth_ip_and_mask(ip, mask)
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500


@network_bp.route('/connect_to_ap', methods=['POST'])
def connect_to_ap_route():
    try:
        ssid = request.json.get('ssid')
        password = request.json.get('password')

        if not ssid or not password:
            return jsonify({'error': 'SSID and password are required'}), 400

        result = connect_to_new_ap(ssid, password)
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500