import network
import time
import ntptime
import csvwriter

wlan = network.WLAN(network.STA_IF)

def do_connect():
    global wlan
    wlan.active(True)
    wlan.disconnect()
    time.sleep(1)
    if not wlan.isconnected():
        print('do scan...')
        print('wifis:', wlan.scan())
        print('connecting to network...')
        wlan.connect("WI-7-2.4", "inov84ever")
        while not wlan.isconnected():
            time.sleep(1)
            print('...')
            pass
    print('network config:', wlan.ifconfig())

do_connect()

ntptime.settime()

csvwriter.readPlatesFromFile()




