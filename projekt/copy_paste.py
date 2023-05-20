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