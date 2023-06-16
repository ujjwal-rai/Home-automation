import multiprocessing

def run_file1():
    import RPi.GPIO as GPIO
    import time

    # Define GPIO pins for the IR sensors and LED
    SENSOR_1_PIN = 12
    SENSOR_2_PIN = 10
    lcd = 37
    lcd2 =35
    flag = 0
    flag2 =0
    in1 = 11
    in2 = 13
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(SENSOR_1_PIN, GPIO.IN)
    GPIO.setup(SENSOR_2_PIN, GPIO.IN)
    GPIO.setup(lcd, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(lcd2, GPIO.OUT)
  

    

    
  
    # Set up GPIO mode and pins
    

  
    # Create initial empty list of people in the room
    person_in_room = []



    # Define function to update person_in_room list based on sensor readings





    # Loop to check person_in_room list and control LED
    while True:
        if len(person_in_room)>0 :
            flag2=1
        if len(person_in_room)==0 and flag2 == 1 :
            time.sleep(5)
            flag2=0
            GPIO.output(lcd,GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(lcd2,GPIO.LOW)
          
            
            
        if GPIO.input(SENSOR_1_PIN) == GPIO.LOW and flag==0:
        # Sensor 1 detected first, then sensor 2, so add 1 person to the list
            flag=1
            #print("aagya")
        if GPIO.input(SENSOR_2_PIN) == GPIO.LOW and flag==1:
            flag=0
            #print("idhar bhi aa gaya")
            person_in_room.append(0)
            time.sleep(1)
        if GPIO.input(SENSOR_2_PIN) == GPIO.LOW and flag==0:
            # Sensor 2 detected first, then sensor 1, so remove 1 person from the list
            flag=2
        if GPIO.input(SENSOR_1_PIN) == GPIO.LOW and flag==2:
            flag=0
            if len(person_in_room) > 0:
                person_in_room.pop()
            time.sleep(1)
        #print(person_in_room)
    
        print(person_in_room)
    

# Clean up GPIO pins
    GPIO.cleanup()
    # add code to run your first Python file here

def run_file2():
    
    #!/usr/bin/env python3

    import RPi.GPIO as GPIO
    import os
    import time
    from http.server import BaseHTTPRequestHandler, HTTPServer
    
    
    host_name = '192.168.120.164'  # IP Address of Raspberry Pi
    host_port = 8095
   
    
    # Set up GPIO mode and pin number

    # Define function to turn LED on
    def led_on():
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(37, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)

        GPIO.output(35, GPIO.HIGH)


        GPIO.output(37, GPIO.HIGH)

# Define function to turn LED off
    def led_off():
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(35, GPIO.OUT)
        GPIO.output(35, GPIO.LOW)
        GPIO.setup(37, GPIO.OUT)

        GPIO.output(37, GPIO.LOW)
    

    

    class Motor():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        def __init__(self,Ena,In1,In2):
            self.Ena = Ena
            self.In1 = In1
            self.In2 = In2
            GPIO.setup(self.Ena, GPIO.OUT)
            GPIO.setup(self.In1, GPIO.OUT)
            GPIO.setup(self.In2, GPIO.OUT)
            self.pwm = GPIO.PWM(self.Ena, 100)
            self.pwm.start(0)

        def move(self, x=0):
            GPIO.output(self.In1, GPIO.LOW)
            GPIO.output(self.In2, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(x)

    motor1 = Motor(15, 13, 11)




        
        


    def getTemperature():
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        return temp


    class MyServer(BaseHTTPRequestHandler):

        def do_HEAD(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def _redirect(self, path):
            self.send_response(303)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', path)
            self.end_headers()

        def do_GET(self):
            html = '''<!DOCTYPE html>
                <html lang="en" dir="ltr">
                <head>
                <meta charset="utf-8">
                <title></title>
                <style media="screen">
                .answer {{
                    background-color: #11cdd4;
                    font-size: 60px;
                    border-style: none;
                    margin: 30px 30px 30px 30px;
                    border-radius: 10px;
                    padding: 5px 20px 5px 20px;
                    color: #02444a;
                  }}
                  input:hover {{
                  background-color: #30e3cb;
                  }}
                  p {{
                 font-size: 65px;
                 color: #02444a;
                 font-weight: bold;
                 font-style: oblique;  
                 font-family: "Copperplate", "Copperplate", Fantasy;
             }}
              h1 {{
                font-size: 75px;
                color: #02444a;
                margin: 30px auto 400px auto;
                  }}
            </style>
            </head>
            <body bgcolor="#cffaf9">
            <center><h1><u>Welcome to the Room</u></h1>
            <p>Light</p><form action="/" method="POST">
            <input type="submit" name="submit" class="answer" value="Low">
            <input type="submit" name="submit" class="answer" value="Medium">
            <input type="submit" name="submit" class="answer" value="High">
            </form> <br><p>LCD</p><form action="/" method="POST">
            <input type="submit" name="submit" class="answer" value="ON">
            <input type="submit" name="submit" class="answer" value="OFF">
            </form> <br><p>Fan Speed</p><form action="/" method="POST">
            <input type="submit" name="submit" class="answer" value="0">
            <input type="submit" name="submit" class="answer" value="1">
            <input type="submit" name="submit" class="answer" value="2">
            <input type="submit" name="submit" class="answer" value="3">
            <input type="submit" name="submit" class="answer" value="4"></form></center>
            </body>
            </html>'''
            temp = getTemperature()
            self.do_HEAD()
            self.wfile.write(html.format(temp[5:]).encode("utf-8"))

        def do_POST(self):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            post_data = post_data.split("=")[1]
            
            if post_data =="ON":
                led_on()
                print("on ho gyi led")
            elif post_data == 'OFF':
                led_off()
                print("off led ho gyyi")
            elif post_data == '0':
                
                motor1.move(0)
               
                
            elif post_data == '1':
               
                motor1.move(20)
               
            elif post_data == '2':
               
                motor1.move(40)
                
            elif post_data == '3':
                
                motor1.move(75)
                
            elif post_data == '4':
                
                motor1.move(100)
                
            elif post_data == 'Low':
                set_brightness('low')
                print("low")
               
            elif post_data == 'Medium':
                set_brightness('medium')
                print("Medium")
               
            elif post_data == 'High':
                set_brightness('high')
                print("high") 
            print("LED is {}".format(post_data))
            self._redirect('/')  # Redirect back to the root url


    # # # # # Main # # # # #

    if __name__ == '__main__':
        http_server = HTTPServer((host_name, host_port), MyServer)
        print("Server Starts - %s:%s" % (host_name, host_port))

        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            http_server.server_close()
        # add code to run your second Python file here

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_file1)
    p2 = multiprocessing.Process(target=run_file2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
