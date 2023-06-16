import multiprocessing

def run_file1():
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BOARD)
    sensor_pin = 24
    buzzer_pin = 26
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    while True:
        if GPIO.input(sensor_pin)== GPIO.LOW :
            GPIO.output(buzzer_pin,GPIO.HIGH)
            print("ok")
            time.sleep(10)
        else:
            GPIO.output(buzzer_pin,GPIO.LOW)
            print("omk")


    # add code to run your first Python file here

def run_file2():
    
#!/usr/bin/env python3

    import RPi.GPIO as GPIO
    import os
    import time
    from http.server import BaseHTTPRequestHandler, HTTPServer

    host_name = '192.168.110.164'  # IP Address of Raspberry Pi
    host_port = 8002
    # Function to alert the buzzer for 10 seconds when IR sensor reads digital high



    def set_servo_angle(servo_pin, angle):
        # Set up GPIO pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)

        # Set up PWM for servo signal
        pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)
        pwm.start(0)  # start with 0% duty cycle

        # Map angle to duty cycle
        duty_cycle = angle / 18 + 2.5  # 0 deg = 2.5% duty cycle, 180 deg = 12.5% duty cycle

        # Set servo to desired angle
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # allow time for servo to move to new position

        # Clean up GPIO pins
        pwm.stop()
        GPIO.cleanup()


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
            html = '''
                <html>
                <style media="screen">
                .answer {{
                    background-color: #11cdd4;
                    font-size: 70px;
                    border-style: none;
                    margin: 30px auto 30px auto;
                    border-radius: 10px;
                    padding: 5px 20px 5px 20px;
                    color: #02444a;
                }}
                    input:hover {{
                    background-color: #30e3cb;
                }}
                p {{
                    font-size: 55px;
                    color: #02444a;
                }}
                h1 {{
                    font-size: 75px;
                    color: #02444a;
                }}
                </style>
               <body style="width:960px; margin: 20px auto;" topmargin="40px">
               <center><h1>Lock and Unlock the main door.</h1></center>
               <center><form action="/" method="POST">
                  <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br> <p>Main Door :</p>
                   <input type="submit" name="submit" class= "answer" value="Unlock" size="5"><br><br><br>
                   <input type="submit" name="submit" class= "answer" value="Lock" size="5">
               </form></center>
               </body>
               </html>
            '''
            temp = getTemperature()
            self.do_HEAD()
            self.wfile.write(html.format(temp[5:]).encode("utf-8"))

        def do_POST(self):

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            post_data = post_data.split("=")[1]
            
           
            if post_data == 'Lock':
                set_servo_angle(36,0)
               
                
            else:
                set_servo_angle(36,120)
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
