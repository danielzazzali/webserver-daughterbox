from flask import Flask, render_template

from config.config import load_env, get_env_variable
from controllers.mode_controller import mode_bp
from controllers.network_controller import network_bp
from models.network_model import remembered_connections, scan_wifi_networks, get_active_wifi_network

load_env()

port = int(get_env_variable('PORT'))

app = Flask(__name__)

app.register_blueprint(network_bp)
app.register_blueprint(mode_bp)

@app.route('/')
def index():
    return render_template('index.html')

def test_api():
    with app.test_client() as client:

        response_ip = client.get('/ip')
        print(response_ip.get_json())

        response_mode = client.get('/mode')
        print(response_mode.get_json())

        new_mode = "AP"
        #response_set_mode = client.post('/mode', json={'mode': new_mode})
        #print(response_set_mode.get_json())

        #response_rem_conn = client.get('/remembered_connections')
        #print(response_rem_conn.get_json())

        #response_scan_wifi = client.get('/scan_wifi_networks')
        #print(response_scan_wifi.get_json())

        #response_active_wifi = client.get('/active_wifi_network')
        #print(response_active_wifi.get_json())

        connection_to_delete = "AAAA"
        #response_delete_connection = client.post('/delete_connection', json={'connection_name': connection_to_delete})
        #print(response_delete_connection.get_json())

        connection_to_connect = "AP"
        #response_connect_to_network = client.post('/connect_to_network', json={'connection_name': connection_to_connect})
        #print(response_connect_to_network.get_json())

        connection_to_disconnect = "AP"
        #response_disconnect_from_network = client.post('/disconnect_from_network', json={'connection_name': connection_to_disconnect})
        #print(response_disconnect_from_network.get_json())

        connection_to_autoconnect = "AP"
        #response_set_autoconnect_off = client.post('/set_autoconnect_off', json={'connection_name': connection_to_autoconnect})
        #print(response_set_autoconnect_off.get_json())

        #response_set_autoconnect_on = client.post('/set_autoconnect_on', json={'connection_name': connection_to_autoconnect})
        #print(response_set_autoconnect_on.get_json())

        #response_eth_ip = client.get('/eth_ip')
        #print(response_eth_ip.get_json())

        new_ip = "172.16.23.23"
        new_mask = "24"
        #response_set_eth_ip_and_mask = client.post('/set_ip', json={'ip': new_ip, 'mask': new_mask})
        #print(response_set_eth_ip_and_mask.get_json())

        new_ap = "zzz"
        new_password = "12345678"
        response_connect_to_new_ap = client.post('/connect_to_ap', json={'ssid': new_ap, 'password': new_password})
        print(response_connect_to_new_ap.get_json())


if __name__ == '__main__':
    test_api()
    #app.run(port=port)
