import binascii
import pygatt
import pygatt.backends
import struct
import threading

SPEED_FEET_PER_REVOLUTION = 1.0924137931
DISTANCE_FEET_PER_REVOLUTION = 5.16667 # 10 inches
DISTANCE_FEET_PER_REVOLUTION = 6.9
FEET_PER_MILE = 5280

counter_lock = threading.Lock()
PREVIOUS_RAW_DIST = -1
COUNTER = 0 

def _2ad2_handler(handle, value):
    data = value.hex()
    flag = data[0:4]
    cadence = data[4:8]
    resistance = data[8:12]
    idk = data[12:]

    enc = binascii.unhexlify(cadence)
    cadence = int.from_bytes(enc, 'little')
    cadence = cadence / 2

    enc = binascii.unhexlify(resistance)
    resistance = int.from_bytes(enc, 'little', signed=True)
    

    mph = (cadence * SPEED_FEET_PER_REVOLUTION * 60) / FEET_PER_MILE

    mph = round(mph, 1)

    print("mph: {}".format(mph))


def _2a5b_handler(handle, value):
    global COUNTER
    global PREVIOUS_RAW_DIST 

    data = value.hex()
    flag = data[0:2]
    cumulative_revolutions = data[2:10]
    last_wheel_event_time = data[10:14]
    cum_crank_revolution = data[14:18]
    last_crank_event_time = data[18:]

    enc = binascii.unhexlify(cumulative_revolutions)
    uint32_cum_rev = int.from_bytes(enc, byteorder='little')

    with counter_lock:
        if PREVIOUS_RAW_DIST == -1:
            PREVIOUS_RAW_DIST = uint32_cum_rev
        diff = uint32_cum_rev - PREVIOUS_RAW_DIST
        COUNTER += diff
        PREVIOUS_RAW_DIST = uint32_cum_rev

    enc = binascii.unhexlify(last_wheel_event_time)
    uint16_wheel_time = int.from_bytes(enc, byteorder='little')
    uint16_wheel_time = uint16_wheel_time * 2 ** -10

    enc = binascii.unhexlify(cum_crank_revolution)
    uint16_crank_revolution = int.from_bytes(enc, byteorder='little')

    enc = binascii.unhexlify(last_crank_event_time)
    uint16_crank_time = int.from_bytes(enc, byteorder='little')
    uint16_crank_time = uint16_crank_time * 2 ** -10

    distance = round(COUNTER * DISTANCE_FEET_PER_REVOLUTION / FEET_PER_MILE, 2)
    print("Distance: {}".format(distance))

bd_addr = "DD:F5:95:47:82:95"
_2a5b_characteristic = "00002a5b-0000-1000-8000-00805f9b34fb"
_2ad2_characteristic = "00002ad2-0000-1000-8000-00805f9b34fb"

ADDRESS_TYPE = pygatt.BLEAddressType.random

adapt = pygatt.GATTToolBackend()
adapt.start()
device = adapt.connect(bd_addr, address_type=ADDRESS_TYPE)

try:
    device.subscribe(_2a5b_characteristic, callback=_2a5b_handler)
    device.subscribe(_2ad2_characteristic, callback=_2ad2_handler)
    input("Press enter to stop program...\n")
finally:
    adapt.stop()
