import csv
import functions
import time
import sys
import math
from smbus import SMBus

busNum = 1
b = SMBus(busNum)
LSM = 0x1d #address on the raspberry pi
LSM_WHOAMI = 0b1001001 #Device self-id

LPS = 0x5d #address on the raspberry pi
LPS_WHOAMI = 0b10111101 #Device self-id

L3G = 0x6b #address on the raspberry pi
L3G_WHOAMI = 0b11010111 #Device self-id

if b.read_byte_data(LSM, 0x0f) == LSM_WHOAMI:
    print('LSM303D detected successfully.')
else:
    print('No LSM303D detected on bus '+str(busNum)+'.')
    sys.exit()

if b.read_byte_data(LPS, 0x0f) == LPS_WHOAMI:
    print('LPS25H detected successfully.')
else:
    print('No LPS25H detected on bus '+str(busNum)+'.')
    sys.exit()

if b.read_byte_data(L3G, 0x0f) == L3G_WHOAMI:
    print('L3GD20H detected successfully.')
else:
    print('No L3GD20H detected on bus '+str(busNum)+'.')
    sys.exit()

#the functions used
twosCompCombine = functions.twos_comp_combine   #takes two arguments
twosCompCombine12Bit = functions.twos_comp_combine_12   #takes two arguments
celsiusToFahrenheit = functions.c_to_f  #takes one argument
convertMag = functions.convert_mag      #takes one argument
convertAcc = functions.convert_acc      #takes one argument
convertGyro = functions.convert_gyro    #takes one argument
convertBarometer = functions.convert_barometer  #takes one argument
convertTemp = functions.convert_temp    #takes one argument
convertTempLPS = functions.convert_temp_LPS # takes one argument
vectorLength = functions.vector_length  #takes three agruments

#Storing the accelerometer readings in a list
#roll=[0,0]
#pitch=[0,0]
#yaw=[0,0]

#Control register addresses -- from LSM303D datasheet(acc and mag)
LSM_CTRL_0 = 0x1F #General settings
LSM_CTRL_1 = 0x20 #Turns on accelerometer and configures data rate
LSM_CTRL_2 = 0x21 #Self test accelerometer, anti-aliasing accel filter
LSM_CTRL_3 = 0x22 #Interrupts
LSM_CTRL_4 = 0x23 #Interrupts
LSM_CTRL_5 = 0x24 #Turns on temperature sensor
LSM_CTRL_6 = 0x25 #Magnetic resolution selection, data rate config
LSM_CTRL_7 = 0x26 #Turns on magnetometer and adjusts mode

#Control register addresses -- from L3GD20H datasheet (GYRO)
L3G_CTRL_1 = 0x20 #Turns on Gyro and configures data rate
L3G_CTRL_2 = 0x21 #Filter mode and edge or level sensitive enable
L3G_CTRL_3 = 0x22 #Interrupts
L3G_CTRL_4 = 0x23 #Interrupts and also self test
L3G_CTRL_5 = 0x24 #General settings

#LSM303D
#Registers holding twos-complemented MSB and LSB of magnetometer readings -- from LSM303D datasheet
MAG_X_LSB = 0x08 # x
MAG_X_MSB = 0x09
MAG_Y_LSB = 0x0A # y
MAG_Y_MSB = 0x0B
MAG_Z_LSB = 0x0C # z
MAG_Z_MSB = 0x0D

#Registers holding twos-complemented MSB and LSB of magnetometer readings -- from LSM303D datasheet
ACC_X_LSB = 0x28 # x
ACC_X_MSB = 0x29
ACC_Y_LSB = 0x2A # y
ACC_Y_MSB = 0x2B
ACC_Z_LSB = 0x2C # z
ACC_Z_MSB = 0x2D

#L3GD20H
#Registers holding twos-complemented gyro readings -- L3GD20H datasheet
GYRO_X_L = 0x28 #X
GYRO_X_H = 0x29
GYRO_Y_L = 0x2A #Y
GYRO_Y_H = 0x2B
GYRO_Z_L = 0x2C #Z
GYRO_Z_H = 0x2D

#setting the IMU to the correct settings
b.write_byte_data(LSM, LSM_CTRL_1, 0b01010111) # enable accelerometer, 50 hz sampling
b.write_byte_data(LSM, LSM_CTRL_2, 0x00) #set +/- 2g full scale
b.write_byte_data(LSM, LSM_CTRL_5, 0b11100100) #high resolution mode, thermometer on, 6.25hz ODR
b.write_byte_data(LSM, LSM_CTRL_7, 0b00010000) #get magnetometer out of low power mode, and enables thermometer to take readings

#sleep while it is being put into rocket
time.sleep(5) #sleeps for 15 seconds before taking readings


#take initial readings
accx = twosCompCombine(b.read_byte_data(LSM, ACC_X_MSB), b.read_byte_data(LSM, ACC_X_LSB))
accy = twosCompCombine(b.read_byte_data(LSM, ACC_Y_MSB), b.read_byte_data(LSM, ACC_Y_LSB))
accz = twosCompCombine(b.read_byte_data(LSM, ACC_Z_MSB), b.read_byte_data(LSM, ACC_Z_LSB))
#convert to usable values
accx = convertAcc(accx)
accy = convertAcc(accy)
accz = convertAcc(accz)

#Seperate Accelerations

roll=math.atan2(accx,math.sqrt(math.pow(accy,2)+math.pow(accz,2)))
pitch=math.atan2(accy,math.sqrt(math.pow(accx,2)+math.pow(accz,2)))
yaw=math.atan2(math.sqrt(math.pow(accx,2)+math.pow(accy,2)),accz)

roll=roll*180/math.pi
pitch=pitch*180/math.pi
yaw=yaw*180/math.pi

#Single Value Accelerations

overallAcc = vectorLength(roll,pitch,yaw)

#for Gyro(L3GD20H)
b.write_byte_data(L3G, 0x39, 0b00001) #sets ODR to 1
b.write_byte_data(L3G, L3G_CTRL_1, 0b11101111) #enables gyro 50HZ sampling ODR and 16.6 HZ cut-off
b.write_byte_data(L3G, L3G_CTRL_2, 0x00) #set high pass filter cut off frequency to 4 HZ

gyroxLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_X_H), b.read_byte_data(L3G, GYRO_X_L)))
gyroyLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_Y_H), b.read_byte_data(L3G, GYRO_Y_L)))
gyrozLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_Z_H), b.read_byte_data(L3G, GYRO_Z_L)))

while roll>=45 or roll<=-45 or pitch>=45 or pitch<=-45 :
        print 'Party'      
        accxLoop = convertAcc(twosCompCombine(b.read_byte_data(LSM, ACC_X_MSB), b.read_byte_data(LSM, ACC_X_LSB)))
        accyLoop = convertAcc(twosCompCombine(b.read_byte_data(LSM, ACC_Y_MSB), b.read_byte_data(LSM, ACC_Y_LSB)))
        acczLoop = convertAcc(twosCompCombine(b.read_byte_data(LSM, ACC_Z_MSB), b.read_byte_data(LSM, ACC_Z_LSB)))
        overallAccLoop = vectorLength(accxLoop, accyLoop, acczLoop)    #Single Acceleration Value
        roll=math.atan2(accxLoop,math.sqrt(math.pow(accyLoop,2)+math.pow(acczLoop,2)))
        pitch=math.atan2(accyLoop,math.sqrt(math.pow(accxLoop,2)+math.pow(acczLoop,2)))
        yaw=math.atan2(math.sqrt(math.pow(accxLoop,2)+math.pow(accyLoop,2)),acczLoop)
        roll=roll*180/math.pi
        pitch=pitch*180/math.pi
        yaw=yaw*180/math.pi
        #takes Gyro readings then converts to usable values in one line
        gyroxLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_X_H), b.read_byte_data(L3G, GYRO_X_L)))
        gyroyLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_Y_H), b.read_byte_data(L3G, GYRO_Y_L)))
        gyrozLoop = convertGyro(twosCompCombine(b.read_byte_data(L3G, GYRO_Z_H), b.read_byte_data(L3G, GYRO_Z_L)))
        #overallGyroLoop = vectorLength(gyroxLoop, gyroyLoop, gyrozLoop)   
        break             
#Exits the loop
print("Done")

























