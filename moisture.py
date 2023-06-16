import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BOARD)
# Set up GPIO
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


# Define motor control pins

IN3 = 21
IN4 = 23

# Define motor functions
def move_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

# Set up GPIO pin 3 as an input
GPIO.setup(3, GPIO.IN)

# Loop to continuously read input value
while True:
    # Read the input value at GPIO pin 3
    input_value = GPIO.input(3)

    # Print the input value
    print("Input value: {}".format(input_value))
    if input_value == 1 :
        move_forward()
    elif input_value ==0 :
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        
    # Wait for 1 second
    time.sleep(1)

# Clean up the GPIO pins
GPIO.cleanup()
