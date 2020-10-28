''' myspinclass.routes.bluetooth_endpoints
'''
from flask import Blueprint

ble_bp = Blueprint('ble', __name__)

@ble_bp.route('/bluetooth/list-devices', methods=['GET'])
def bluetooth_search():
    pass

@ble_bp.route('/bluetooth/connect-device', methods=['GET'])
def bluetooth_connect():
    pass

@ble_bp.route('bluetooth/<device>/disconnect', methods=['GET'])
def bluetooth_disconnect(device):
    pass

@ble_bp.route('/bluetooth/<device>/services', methods=['GET'])
def bluetooth_services(device):
    pass

@ble_bp.route('/bluetooth/<device>/<service>/characteristics', methods=['GET'])
def bluetooth_characteristic_list(device, service):
    pass

@ble_bp.route('/bluetooth/<device>/<service>/<characteristic>', methods=['GET'])
def bluetooth_connect_characteristic(device, service, characteristic):
    pass

