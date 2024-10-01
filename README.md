---

# Raspberry Pi Projects for Sensor and Motor Control

This repository contains multiple Python projects using Raspberry Pi GPIO pins to interact with various sensors and devices, including motors, IR sensors, and buzzers. Each project demonstrates a different application, from simple motor control to an advanced alarm system.

## Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [Software Requirements](#software-requirements)
3. [Project 1: Motor Control with Input Monitoring](#project-1-motor-control-with-input-monitoring)
4. [Project 2: Buzzer Alarm with IR Sensor](#project-2-buzzer-alarm-with-ir-sensor)
5. [Project 3: Door Lock Control with Web Server](#project-3-door-lock-control-with-web-server)
6. [Project 4: Sensor-based Alarm System](#project-4-sensor-based-alarm-system)
7. [Running the Code](#running-the-code)

## Hardware Requirements
- **Raspberry Pi**
- **IR Sensor**
- **Buzzer**
- **Servo Motor**
- **DC Motor Driver Module**
- **Push Buttons**
- **Wires and power supply**

## Software Requirements
- **Python 3.x**
- **RPi.GPIO Library**

To install the RPi.GPIO library if it’s not already installed:
```bash
pip install RPi.GPIO
```

## Project 1: Motor Control with Input Monitoring

### Description
This project demonstrates how to control a DC motor based on the input from a GPIO pin. The motor will run forward when a button is pressed and stop when the button is released.

### Code Overview
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Set up GPIO pins for the motor control
GPIO.setup(21, GPIO.OUT)  # Motor control pin 1
GPIO.setup(23, GPIO.OUT)  # Motor control pin 2
GPIO.setup(3, GPIO.IN)     # Button input pin

def move_forward():
    GPIO.output(21, GPIO.HIGH)  # Activate motor
    GPIO.output(23, GPIO.LOW)   # Set motor direction

# Continuous loop to monitor button state
while True:
    input_value = GPIO.input(3)  # Read button state
    if input_value == 1:
        move_forward()             # Move forward if button pressed
    else:
        GPIO.output(21, GPIO.LOW)  # Stop motor
        GPIO.output(23, GPIO.LOW)

    time.sleep(1)

# Clean up GPIO pins
GPIO.cleanup()
```

### Explanation
- Uses GPIO pin 21 and 23 to control a DC motor.
- Reads input from GPIO pin 3 (a button).
- The motor moves forward when the button is pressed and stops when released.

## Project 2: Buzzer Alarm with IR Sensor

### Description
This project uses an IR sensor to monitor if an object is present. If an object is not detected for a specified time, a buzzer will sound to alert the user.

### Code Overview
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pin for the IR sensor and buzzer
ir_pin = 18
GPIO.setup(ir_pin, GPIO.IN)
buzzer_pin = 22
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

last_seen = time.time()
time_threshold = int(input("How much time you can leave your dish or set an alarm: "))

while True:
    if GPIO.input(ir_pin) == GPIO.LOW:
        last_seen = time.time()  # Update last seen time
        GPIO.output(buzzer_pin, GPIO.LOW)  # Turn off buzzer
    else:
        if time.time() - last_seen > time_threshold:
            GPIO.output(buzzer_pin, GPIO.HIGH)  # Activate buzzer
        else:
            GPIO.output(buzzer_pin, GPIO.LOW)  # Deactivate buzzer

    time.sleep(0.1)
```

### Explanation
- Monitors the state of an IR sensor connected to GPIO pin 18.
- If no object is detected for a specified time (`time_threshold`), the buzzer connected to pin 22 is activated.

## Project 3: Door Lock Control with Web Server

### Description
This project sets up a web server on the Raspberry Pi that allows users to lock and unlock a door using a web interface. A servo motor controls the locking mechanism.

### Code Overview
```python
import RPi.GPIO as GPIO
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.110.164'
host_port = 8002

def set_servo_angle(servo_pin, angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    duty_cycle = angle / 18 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        html = '''<html>
                  <form action="/" method="POST">
                  <input type="submit" name="submit" value="Unlock">
                  <input type="submit" name="submit" value="Lock">
                  </form></html>'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        command = post_data.split("=")[1]

        if command == 'Lock':
            set_servo_angle(36, 0)
        else:
            set_servo_angle(36, 120)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    http_server.serve_forever()
```

### Explanation
- Sets up a web server that allows users to lock/unlock a door using servo motor control via a web interface.
- Uses a simple HTML form to send commands to the Raspberry Pi.

## Project 4: Sensor-based Alarm System

### Description
This project utilizes an IR sensor to monitor if an object is present and activates a buzzer if the object is not detected for a specific duration.

### Code Overview
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pin for the IR sensor and buzzer
ir_pin = 18
GPIO.setup(ir_pin, GPIO.IN)
buzzer_pin = 22
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

last_seen = time.time()
time_threshold = int(input("How much time you can leave your dish or set an alarm: "))

while True:
    if GPIO.input(ir_pin) == GPIO.LOW:
        last_seen = time.time()  # Update last seen time
        GPIO.output(buzzer_pin, GPIO.LOW)  # Turn off buzzer
    else:
        if time.time() - last_seen > time_threshold:
            GPIO.output(buzzer_pin, GPIO.HIGH)  # Activate buzzer
        else:
            GPIO.output(buzzer_pin, GPIO.LOW)  # Deactivate buzzer

    time.sleep(0.1)
```

### Explanation
- Similar to Project 2, this project checks the status of an IR sensor and activates a buzzer if an object is not detected for too long.

## Running the Code

To run any of the projects on your Raspberry Pi, navigate to the project directory and execute the following command:
```bash
python3 <filename>.py
```

Ensure that all hardware components are connected to the designated GPIO pins as specified in each project.

## Conclusion
This repository showcases practical applications of Raspberry Pi for sensor and motor control, demonstrating how to create interactive systems for real-world use cases.

--- 
