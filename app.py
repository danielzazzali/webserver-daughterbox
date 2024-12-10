from flask import Flask, render_template

from config.constants import PORT
from controllers.device_mode_controller import mode_bp
from controllers.ethernet_controller import ethernet_bp
from controllers.wifi_controller import wifi_bp


port = int(PORT)
app = Flask(__name__)
app.register_blueprint(mode_bp)
app.register_blueprint(ethernet_bp)
app.register_blueprint(wifi_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/no_camera/')
def no_camera():
    return render_template('no_camera.html')

if __name__ == '__main__':
    app.run(port=port)
