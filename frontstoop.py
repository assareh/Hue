#!/usr/bin/env python

""" This script checks the front stoop floods every minute at night and if
    they are off, turns them on to 1%. Then during the day checks if they
    are on and turns them off until night. """

import os
import signal
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ON_PAYLOAD = "{\n    \"on\": true,\n    \"bri\":2\n}"
OFF_PAYLOAD = "{\n    \"on\": false\n}"
API_KEY = os.environ['HUE_API_KEY']
URL28 = "https://hue-bridge/api/" + API_KEY + "/sensors/28"
URL12 = "https://hue-bridge/api/" + API_KEY + "/lights/12/"
URL13 = "https://hue-bridge/api/" + API_KEY + "/lights/13/"
signal.signal(signal.SIGINT, signal.default_int_handler)


def dark_outside():
    ''' return true if it's dark outside, false if it's daylight '''
    response = requests.request("GET", URL28, verify=False)
    return response.json()['state']['dark']


def is_off(url):
    ''' return true if light is off, false if it's on
        accepts the url of the light as parameter '''
    response = requests.request("GET", url, verify=False)
    return not response.json()['state']['on']


def turn_on(url):
    ''' turn on flood light
        accepts the url of the light as parameter '''
    requests.request("PUT", url+'state', data=ON_PAYLOAD, verify=False)


def turn_off(url):
    ''' turn off flood light
        accepts the url of the light as parameter '''
    requests.request("PUT", url+'state', data=OFF_PAYLOAD, verify=False)


while True:
    try:
        while dark_outside():
            for FLOOD in [URL12, URL13]:
                if is_off(FLOOD):
                    turn_on(FLOOD)

            time.sleep(60)

        while not dark_outside():
            for FLOOD in [URL12, URL13]:
                if not is_off(FLOOD):
                    turn_off(FLOOD)

            time.sleep(60*30)

    except KeyboardInterrupt:
        print "Exiting..."
        sys.exit()
