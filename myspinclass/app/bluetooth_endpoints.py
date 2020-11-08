''' myspinclass.routes.bluetooth_endpoints
'''
from flask import Blueprint
from pygatt.exceptions import NotConnectedError
from myspinclass.app.connections import DeviceConnection
from myspinclass.app.constants import TEST_DEVICE
import json

ble_bp = Blueprint('ble', __name__)
connection = DeviceConnection()

@ble_bp.route('/bluetooth/list-devices', methods=['GET'])
def bluetooth_search():
   return json.dumps({
        "devices" : connection.scan()
    })
@ble_bp.route('/bluetooth/connect/<device>', methods=['GET'])
def bluetooth_connect(device):
    try:
        device = connection.connect(device)
    except NotConnectedError:
        return "Failure"
    return "Success"

@ble_bp.route('/bluetooth/<device>/disconnect', methods=['GET'])
def bluetooth_disconnect(device):
    pass

@ble_bp.route('/bluetooth/<device>/services', methods=['GET'])
def bluetooth_services(device):
    pass
@ble_bp.route('/bluetooth/device/characteristics', methods=['GET'])
def bluetooth_characteristic_list():
    return connection.scan_characteristics()

@ble_bp.route('/bluetooth/<device>/<service>/<characteristic>', methods=['GET'])
def bluetooth_connect_characteristic(device, service, characteristic):
    pass

