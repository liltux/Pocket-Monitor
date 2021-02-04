gc.collect()

## Simple software WDT implementation
wdt_counter = 0

def wdt_callback():
    global wdt_counter
    wdt_counter += 1
    if (wdt_counter >= 10):
        machine.deepsleep()

def wdt_feed():
    global wdt_counter
    wdt_counter = 0

wdt_timer = machine.Timer(-1)
wdt_timer.init(period=30000, mode=machine.Timer.PERIODIC, callback=lambda t:wdt_callback())
## END Simple software WDT implementation

def get_AirComp_data(url):
    # Bring in Global Variables
    global airPress, airState, airStatus, airSched

    # Get data from HTTP GET request
    try:
        res = urequests.get(url)
    # Store the Json data as a Python Dict
        data = ujson.loads(res.text)
    except:
        oled.clear()
        oled.text('{0}'.format(e), 5, 10)
        oled.text('Server Connect', 0, 20)
        oled.text('Failed', 10, 30)
        oled.text('Reset or Toggle', 0, 40)
        oled.show()
        sleep(1)
        return

    # Make the values easier to read
    airPress = data['AirPressure']
    airState = data['AirState']
    airStatus = data['AirStatus']
    airSched = data['AirScheduler']
    res.close()

    # Display data to OLED
    oled.clear()
    oled.text('PSI: {0}'.format(airPress), 0, 15)
    oled.text('State: {0}'.format(airState), 0, 25)
    oled.text('Stat: {0}'.format(airStatus), 0, 35)
    oled.text('{0}'.format(airSched), 0, 45)
    oled.show()

    return airState, airPress, airStatus, airSched

def AirComp_TurnOnOFF(url, on_url):
    # Bring in Globals
    global airPress, airState, airStatus, airSched

    # Get data to see if Unit is in Auto
    get_AirComp_data(url)

    # If not in Auto, lets start the compressor
    if airState != "In Auto" :
        try:
            air_on = urequests.get(on_url)
            sleep(.5)
            air_on.close()
        except OSError as e:
            oled.clear()
            oled.text('Error.....', 0, 15)
            oled.text('Is Not On?', 10, 25)
            oled.text('Toggle Again?', 0, 35)
            oled.show()
            sleep(1)
            pass
    else :
        try:
            air_off = urequests.get(off_url)
            sleep(.5)
            air_off.close()
        except OSError as e:
            oled.clear()
            oled.text('Error.....', 0, 15)
            oled.text('Is Not Off?', 10, 25)
            oled.text('Toggle Again?', 0, 35)
            oled.show()
            sleep(1)
            pass
    return

# Display now connected and retrieving data
oled.clear()
oled.text('WiFi Connected', 0, 20)
oled.text('Getting', 15, 30)
oled.text('Air Info...', 10, 40)
oled.show()
sleep(2)

# Go Get data display
try:
    get_AirComp_data(url)
except OSError as e:
    oled.clear()
    oled.text('Error Detected', 0,5)
    oled.text('Server Connect', 0, 20)
    oled.text('Failed', 10, 30)
    oled.text('Reset or Toggle', 0, 40)
    oled.show()

# Loop to monitor Button Press
while True:
    press = button.value()

    if press == 0 :
        print("Button pressed")
        sleep(.5)
        AirComp_TurnOnOFF(url, on_url)
        sleep(.5)
        get_AirComp_data(url)
        sleep(1)