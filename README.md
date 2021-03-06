# Pocket Monitor

This is a quick pocket monitor I created to retrieve information from a Node-Red server that is operating our shop air compressor remotely and automatically.

## Hardware

The hardware is a simple ESP32 with OLED display.  I used a prepackaged unit purchased online.  It also included a 3D printed case and Lipo battery.

[Link to LILYGO-TTGO_ESP32-OLED](https://www.banggood.com/LILYGO-TTGO-4M-Bytes-32M-bit-Pro-ESP32-OLED-V2_0-WiFi-Module-p-1270552.html?cur_warehouse=CN&rmmds=search)

## Software Summary

Uses Node-Red (server), micropython (ESP32), ssd1306(OLED, from [github/adafruit](https://github.com/adafruit/micropython-adafruit-ssd1306)), html requests (access to api between the ESP32 and Server).

## Process

Store all of your_secrets in a mysecrets.py file.  This would be SSID/Password information and the like.

I setup HTTP get request and response to trigger events and retrieve information. Using simple urequests(url) I am able to monitor with Node-Red and if the correct value is sent I can turn on or off our compressor.  I can also retrieve specific data points as well by editing the responce depending on the information sent to Node-Red and return data specifics such as running state, is On or Off.

When it first starts it trys to connect to one of several AP we have at our shop.  This is done by using the mysecrets file to store a tuple of the SSIDs and PASSWORDs that can be iterated through as each connection times out.  About 5 tries each before moving on.  If it fails to connect to an AP I notify of problem and enter deepsleep.  

If connection is successful it will try to connect to the server using a GET request URL that is also sending information in the URL.  The Server responds with a JSON object of the data.  This data is then displayed to the OLED.

Using the PRG button on the ESP32 board, if pressed, I call a function that will check the state of the air compressor from the Server Data response.  Then, if the air compressor is off, I send a GET request url to turn on the compressor, and if the air compressor is on the same is done to turn off the compressor.  An effective Remote Toggle switch for the air compressor.

## Purpose

This was a simple project to start using and learn HTML requests and how they can be implemented to interface with APIs.