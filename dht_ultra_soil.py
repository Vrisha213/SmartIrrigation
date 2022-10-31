# import required modules
from machine import ADC, Pin
from dht import DHT11, InvalidChecksum
from hcsr04 import HCSR04
import utime

# use variables instead of numbers:
soil = ADC(Pin(26)) # Soil moisture PIN reference
#Calibraton values
sensor = HCSR04(trigger_pin=2, echo_pin=3, echo_timeout_us=10000)
min_moisture=19200
max_moisture=49300
readDelay = 1 # delay between readings

while True:
# read moisture value and convert to percentage into the calibration range
moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture)
# print values
print(&quot;moisture: &quot; + &quot;%.2f&quot; % moisture +&quot;% (adc: &quot;+str(soil.read_u16())+&quot;)&quot;)
utime.sleep(readDelay) # set a delay between reading

13
#pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
# sensor = DHT11(pin)
#t = (sensor.temperature)
#h = (sensor.humidity)
#print(&quot;Temperature: {}&quot;.format(sensor.temperature))
#print(&quot;Humidity: {}&quot;.format(sensor.humidity))

distance = sensor.distance_cm()
print(&#39;Distance:&#39;, distance, &#39;cm&#39;)
utime.sleep(readDelay)