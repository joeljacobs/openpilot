"""Methods for reading system thermal information."""
import urllib2
import urllib
import json
from secret import *

def read_tz(x):
  with open("/sys/devices/virtual/thermal/thermal_zone%d/temp" % x) as f:
    ret = max(0, int(f.read()))
  return ret

thermal = {}
def read_thermal():
  thermal['cpu0'] = read_tz(5)
  thermal['cpu1'] = read_tz(7)
  thermal['cpu2'] = read_tz(10)
  thermal['cpu3'] = read_tz(12)
  thermal['mem'] = read_tz(2)
  thermal['gpu'] = read_tz(16)
  thermal['bat'] = read_tz(29)

read_thermal()
fanspeed = open("/data/data/com.termux/files/tmp/currentfanspeed", "r")
battery = open("/sys/class/power_supply/battery/capacity", "r")
charged = str(battery.read())
batF = 9.0/5.0 * thermal['bat']/1000 + 32
baseURL = "http://api.thingspeak.com/update?api_key=" + thingspeakWriteApi + "&field"
f = urllib2.urlopen(baseURL + "1=" + str(batF) + "&field2=" + str(fanspeed.read()) + "&field3=" + charged)
f.read()
f.close()
print(str(batF)+ " " + charged)


def sendPushover(title='', msg=''):
    data = urllib.urlencode({
        'user': pushoverConfig['user'],
        'token': pushoverConfig['token'],
        'title': title,
        'message': msg
    })

    try:
        req = urllib2.Request(pushoverConfig['api'], data)

        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        print 'Failed much'

        return False

    res = json.load(response)

    if res['status'] != 1:
        print 'Pushover Fail'

if batF > 130:
    sendPushover("Eon Temp", str(batF))
if battery < 10:
    sendPushover("Eon Batt Low", charged)
