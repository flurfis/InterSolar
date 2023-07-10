from machine import ADC
from time import sleep
import machine
from machine import Pin

led = Pin(25, Pin.OUT)
led.value(1)

rtc = machine.RTC()
print(rtc.datetime())

analogIn = ADC(26)
minutes = 0
seconds = 0

def blink(timer):
    led.toggle()

def writeLine(text):
    file = open("voltmeter.txt", "a")
    file.write(text + "\n")
    file.close()
    print(text)

while True:
    sensorValue = analogIn.read_u16()
    time_in_format = rtc.datetime()
    voltage = sensorValue * (3.3 / 65535) * 2
    #writeLine(str(minutes) + "," + str(seconds) + "," + str(voltage))
    writeLine(str(time_in_format) + "," + str(voltage))
    minutes += 1
    sleep(60)


"""
from machine import ADC
from time import sleep

analogIn = ADC(26)
minutes = 0
seconds = 0

def writeLine(text):
    file = open("voltmeter.txt", "a")
    file.write(text + "\n")
    file.close()
    print(text)

while True:
    sensorValue = analogIn.read_u16()
    voltage = sensorValue * (3.3 / 65535)
    writeLine(str(minutes) + "," + str(seconds) + "," + str(voltage))
    seconds += 1
    if (seconds == 60):
        seconds = 0
        minutes += 1
    sleep(1)
"""



#start led
#from machine import Pin
#led = Pin(25, Pin.OUT)
#led.value(1)


"""
from machine import Pin, Timer
led = Pin(25, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
"""