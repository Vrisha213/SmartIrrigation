import machine, time
from machine import Pin

__version__ = &#39;0.2.0&#39;
__author__ = &#39;Roberto S鐠嬶箯chez&#39;
__license__ = &quot;Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0&quot;

class HCSR04:
&quot;&quot;&quot;
Driver to use the untrasonic sensor HC-SR04.
The sensor range is between 2cm and 4m.

7

The timeouts received listening to echo pin are converted to OSError(&#39;Out of range&#39;)
&quot;&quot;&quot;
# echo_timeout_us is based in chip range limit (400cm)
def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
&quot;&quot;&quot;
trigger_pin: Output pin to send pulses
echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
echo_timeout_us: Timeout in microseconds to listen to echo pin.
By default is based in sensor limit range (4m)
&quot;&quot;&quot;
self.echo_timeout_us = echo_timeout_us
# Init trigger pin (out)
self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
self.trigger.value(0)

# Init echo pin (in)
self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

def _send_pulse_and_wait(self):
&quot;&quot;&quot;
Send the pulse to trigger and listen on echo pin.
We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
&quot;&quot;&quot;
self.trigger.value(0) # Stabilize the sensor
time.sleep_us(5)
self.trigger.value(1)
# Send a 10us pulse.
time.sleep_us(10)
self.trigger.value(0)
try:
pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
return pulse_time
except OSError as ex:
if ex.args[0] == 110: # 110 = ETIMEDOUT

8

raise OSError(&#39;Out of range&#39;)
raise ex

def distance_mm(self):
&quot;&quot;&quot;
Get the distance in milimeters without floating point operations.
&quot;&quot;&quot;
pulse_time = self._send_pulse_and_wait()

# To calculate the distance we get the pulse_time and divide it by 2
# (the pulse walk the distance twice) and by 29.1 becasue
# the sound speed on air (343.2 m/s), that It&#39;s equivalent to
# 0.34320 mm/us that is 1mm each 2.91us
# pulse_time // 2 // 2.91 -&gt; pulse_time // 5.82 -&gt; pulse_time * 100 // 582
mm = pulse_time * 100 // 582
return mm

def distance_cm(self):
&quot;&quot;&quot;
Get the distance in centimeters with floating point operations.
It returns a float
&quot;&quot;&quot;
pulse_time = self._send_pulse_and_wait()

# To calculate the distance we get the pulse_time and divide it by 2
# (the pulse walk the distance twice) and by 29.1 becasue
# the sound speed on air (343.2 m/s), that It&#39;s equivalent to
# 0.034320 cm/us that is 1cm each 29.1us
cms = (pulse_time / 2) / 29.1
return cms