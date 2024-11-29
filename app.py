from flask import Flask, render_template

from config.config import load_env, get_env_variable
from config.constants import PORT
from controllers.device_mode_controller import mode_bp
from controllers.ethernet_controller import ethernet_bp
from controllers.wifi_controller import wifi_bp

load_env()
port = int(get_env_variable(PORT))
app = Flask(__name__)
app.register_blueprint(mode_bp)
app.register_blueprint(ethernet_bp)
app.register_blueprint(wifi_bp)

@app.route('/')
def index():
    return render_template('index.html')

def test_api():
    with app.test_client() as client:

        #############################################################################
        ###################### Test the mode API  ###################################
        #############################################################################

        # Test the device mode API
        device_mode = client.get('/device_mode')
        print(device_mode.get_json())

        device_mode = client.post('/device_mode', json={'mode': 'NOTAPNORSTA'})
        print(device_mode.get_json())

        #device_mode = client.post('/device_mode', json={'mode': 'AP'})
        #print(device_mode.get_json())

        #############################################################################
        ###################### Test the ethernet API  ###############################
        #############################################################################

        ethernet_ip_and_mask = client.get('/ethernet_ip_and_mask')
        print(ethernet_ip_and_mask.get_json())

        ethernet_ip_and_mask = client.post('/set_ethernet_ip_and_mask', json={'ip': '172.16.23.24', 'mask': '24'})
        print(ethernet_ip_and_mask.get_json())

        ethernet_ip_and_mask = client.post('/set_ethernet_ip_and_mask', json={'ip': '172.16.23.23', 'mask': '24'})
        print(ethernet_ip_and_mask.get_json())

        #############################################################################
        ###################### Test the wi-fi API  ##################################
        #############################################################################

        wifi_ip_and_mask = client.get('/wifi_ip_and_mask')
        print(wifi_ip_and_mask.get_json())

        remembered_wifi_connections = client.get('/remembered_wifi_connections')
        print(remembered_wifi_connections.get_json())

        scan_wifi_networks = client.get('/scan_wifi_networks')
        print(scan_wifi_networks.get_json())

        active_wifi_network = client.get('/active_wifi_network')
        print(active_wifi_network.get_json())


if __name__ == '__main__':
    test_api()
    #app.run(port=port)
