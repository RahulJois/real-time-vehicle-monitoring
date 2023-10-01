import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.OUT)  #LED to GPIO24
GPIO.setup(16, GPIO.OUT)  #LED to GPIO24
GPIO.setup(20, GPIO.OUT)  #LED to GPIO24
GPIO.setup(21, GPIO.OUT)  #LED to GPIO24


try:
    while True:
         button_state1 = GPIO.input(6)
         button_state2 = GPIO.input(13)
         button_state3 = GPIO.input(19)
         button_state4 = GPIO.input(26)
         if button_state1 == False:
             GPIO.output(12, True)
             print('Button1 Pressed...')
             time.sleep(0.5)
         else:
             GPIO.output(12, False)

         if button_state2 == False:
             GPIO.output(16, True)
             print('Button2 Pressed...')
             time.sleep(0.5)
         else:
             GPIO.output(16, False)

         if button_state3 == False:
             GPIO.output(20, True)
             print('Button3 Pressed...')
             time.sleep(0.5)
         else:
             GPIO.output(20, False)

         if button_state4 == False:
             GPIO.output(21, True)
             print('Button4 Pressed...')
             time.sleep(0.5)
         else:
             GPIO.output(21, False)
except:
    GPIO.cleanup()


