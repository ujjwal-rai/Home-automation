import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# set up the GPIO pin for the IR sensor
ir_pin = 18
GPIO.setup(ir_pin, GPIO.IN)

# set up the GPIO pin for the buzzer
buzzer_pin = 22
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

# set up variables to keep track of time
last_seen = time.time()
time_threshold = int(input("How much time you can leave your dish or/ set an alarm "))
while True:
    
    if GPIO.input(ir_pin) == GPIO.LOW:
        
        last_seen = time.time()
    
        GPIO.output(buzzer_pin, GPIO.LOW)
    else:
        
        if time.time() - last_seen > time_threshold:
          
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
           
            GPIO.output(buzzer_pin, GPIO.LOW)

   
    time.sleep(0.1)
