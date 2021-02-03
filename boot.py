import network
from time import sleep
from machine import Pin, I2C
import ssd1306
import machine
import urequests
import ujson
from mysecrets import secrets
import gc

gc.collect()

# PRG Button assignment
button = machine.Pin(0, machine.Pin.IN)

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(15), sda=Pin(4))
rst = Pin(16, Pin.OUT)
rst.value(1)

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

# Initialize the Display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Display Wake up message
oled.clear()
oled.text('Waking up ....', 0, 25)
oled.show()
sleep(2)

# Assign API URL
url = secrets['URL']
on_url = secrets['OnURL']
off_url = secrets['OffURL']

# Assign networks to connect to
SSID = secrets['ssid']
PASS = secrets['password']

# Initialize air variables
airPress = 'No Data'
airState = 'No Data'
airStatus = 'No Data'
airSched = 'No Data'

# Try to connect to Network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID[0], PASS)

# Notify connecting to network
count = 0
i = 0

while not(sta.isconnected()):
    if i == len(SSID) :
        oled.clear()
        oled.text('No Networks', 0, 15)
        oled.text('Connected!!', 10, 25)
        oled.text('Going to sleep',0, 35)
        oled.show()
        sleep(10)
        machine.deepsleep()

    oled.clear()
    sleep(1)
    oled.text('Connecting ...', 20, 20)
    oled.text('to {0}'.format(SSID[i]), 0, 30)
    oled.show()
    sleep(1)
    count = count + 1

    if count > 5 :
        i = i + 1
        sta.active(False)
        sleep(.5)
        sta.active(True)
        if i >= len(SSID) :
            pass
        else :
            sta.connect(SSID[i], PASS)
            count = 0
        pass