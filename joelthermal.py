"""Methods for reading system thermal information."""
import urllib2
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
batF = 9.0/5.0 * thermal['bat']/1000 + 32
baseURL = "http://api.thingspeak.com/update?api_key=" + thingspeakWriteApi + "&field"
f = urllib2.urlopen(baseURL + "1=" + str(batF) + "&field2=" + str(fanspeed.read()) )
f.read()
f.close()
#for i in thermal:
#    print(thermal[i])
#print(batF)
#print(thermal['bat'])
