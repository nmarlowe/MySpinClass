''' myspinclass.app.connections
'''
import pygatt


class DeviceConnection(Object):
    def __init__(self, mac_addr, address_type=pygatt.BLEAddressType.random):
        self.addr = mac_addr
        self.address_type = address_type
        self.device = None

    def connect(self):
        
        if not self.device:
            adapt = pygatt.GATTToolBackend()
            adapt.start()
            self.device = adapt.connect(self.addr, address_type=self.address_type)
        return self.device

