''' myspinclass.app.connections
'''
import pygatt
import json

class DeviceConnection(object):

    instance = None
    
    class __DeviceConnection(object):
        def __init__(self, address_type=pygatt.BLEAddressType.random):
            self.addr = None
            self.address_type = address_type
            self.adapt = pygatt.GATTToolBackend()
            self.adapt.start()
            self.device = None

    def __init__(self):
        if not DeviceConnection.instance:
            DeviceConnection.instance = DeviceConnection.__DeviceConnection()

    def scan(self):
        devices = DeviceConnection.instance.adapt.scan(run_as_root=True)
        DeviceConnection.instance.adapt.reset()
        return devices

    def connect(self, addr):
        
        DeviceConnection.instance.device = DeviceConnection.instance.adapt.connect(addr, address_type=DeviceConnection.instance.address_type)
        DeviceConnection.instance.addr = addr
        return DeviceConnection.instance.device

    def scan_characteristics(self):
        return json.dumps(DeviceConnection.instance.device.discover_characteristics())
