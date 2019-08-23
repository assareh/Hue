#!/usr/bin/env python

""" This script cycles the color lamps through the rainbow """

import os
import signal
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ON_PAYLOAD = "{\"on\":true, \"sat\":254, \"bri\":254,\"hue\":0}"
OFF_PAYLOAD = "{\n \"on\": false,\n \"xy\": [\n 0.4351,\n 0.4064\n],\n \
                \"sat\":254,\n \"bri\":254,\n \"hue\":0\n}"
API_KEY = os.environ['HUE_API_KEY']
URL1 = "https://hue-bridge/api/" + API_KEY + "/lights/1/state"
URL2 = "https://hue-bridge/api/" + API_KEY + "/lights/2/state"
URL3 = "https://hue-bridge/api/" + API_KEY + "/lights/3/state"
signal.signal(signal.SIGINT, signal.default_int_handler)


def turn_on(url):
    ''' turn on light
        accepts the url of the light as parameter '''
    requests.request("PUT", url, data=ON_PAYLOAD, verify=False)


def turn_off(url):
    ''' turn off light
        accepts the url of the light as parameter '''
    requests.request("PUT", url, data=OFF_PAYLOAD, verify=False)


# initialize lights
for LAMP in [URL1, URL2, URL3]:
    turn_on(LAMP)

# Cycle the hue (hue runs from 0 to 65535)
while True:
    try:
        for i in range(0, 65):
            PAYLOAD = "{\"hue\":" + str(i*1000) + "}"
            for LAMP in [URL1, URL2, URL3]:
                requests.request("PUT", LAMP, data=PAYLOAD, verify=False)

    except KeyboardInterrupt:
        print "Exiting, turning off..."
        for LAMP in [URL1, URL2, URL3]:
            turn_off(LAMP)
        sys.exit()
