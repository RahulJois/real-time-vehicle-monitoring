
import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
port = "/dev/serial0" # the serial port to which the pi is connected.
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while 1:
    try:
        data = ser.readline()
    except:
        print("loading")
#wait for the serial port to churn out data
    if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data
        msg = pynmea2.parse(data)
#parse the latitude and print
        latval = msg.lat
        concatlat = str(latval)
        lat_degrees = degrees =int(concatlat[0:2])+ float(concatlat[2:])/60
#parse the longitude and print
        longval = msg.lon
        concatlong =str(longval)
        long_degrees = int(concatlong[0:3])+ float(concatlong[3:])/60
        break



