#!/usr/bin/env python3

from time import sleep
import os
import sys

from bleson import get_provider, Observer, UUID16
from bleson.logger import log, set_level, ERROR, DEBUG

# Disable warnings
set_level(ERROR)

# # Uncomment for debug log level
# set_level(DEBUG)

# https://macaddresschanger.com/bluetooth-mac-lookup/A4%3AC1%3A38
# OUI Prefix	Company
# A4:C1:38	Telink Semiconductor (Taipei) Co. Ltd.
GOVEE_BT_mac_OUI_PREFIX = "A4:C1:38"

#H5075_UPDATE_UUID16 = UUID16(0xEC88)
H5075_UPDATE_UUID16 = 'UUID16(0xec88)'


govee_devices = {}

# ###########################################################################
FORMAT_PRECISION = ".2f"


# Decode H5075 Temperature into degrees Celcius
def decode_temp_in_c(encoded_data):
    return format((encoded_data / 10000), FORMAT_PRECISION)


# Decode H5075 Temperature into degrees Fahrenheit
def decode_temp_in_f(encoded_data):
    return format((((encoded_data / 10000) * 1.8) + 32), FORMAT_PRECISION)


# Decode H5075 percent humidity
def decode_humidity(encoded_data):
    return format(((encoded_data % 1000) / 10), FORMAT_PRECISION)


from time import gmtime, strftime

# On BLE advertisement callback
def on_advertisement(advertisement):
    
    log.debug(advertisement)

    if advertisement.address.address.startswith(GOVEE_BT_mac_OUI_PREFIX):
        mac = advertisement.address.address
        #print("===>")
        #print(advertisement.uuid16s)
        #print("---------")
        #if mac not in govee_devices:
        #    govee_devices[mac] = {}
        #if H5075_UPDATE_UUID16 in advertisement.uuid16s:
        if len(advertisement.uuid16s)>0:
            current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            # HACK:  Proper decoding is done in bleson > 0.10
            #print(advertisement.name, "Data:", advertisement.mfg_data, "RSSI:", advertisement.rssi)

            print(current_time, advertisement.mfg_data, "RSSI:", advertisement.rssi)



        #log.debug(govee_devices[mac])


# ###########################################################################


adapter = get_provider().get_adapter()

observer = Observer(adapter)
observer.on_advertising_data = on_advertisement

try:
    while True:
        observer.start()
        sleep(2)
        observer.stop()
except KeyboardInterrupt:
    try:
        observer.stop()
        sys.exit(0)
    except SystemExit:
        observer.stop()
        os._exit(0)
