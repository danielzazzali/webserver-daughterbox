from flask import Flask

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
    return "Hello World"

if __name__ == '__main__':
    app.run(port=port)
