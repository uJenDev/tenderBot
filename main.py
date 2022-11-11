import cv2
import pyfirmata
import time
import numpy as np
import socket
import customerSDK, drinksSDK

# Params that allows the program to be tested without camera or robot
# If "robot_connected = False" then you need a program that simulates the robots response
# The directory this code is should contain a program called robotServerSim.py that provides this function

cam_connected = False
robot_connected = False


arduino_port = 'COM4'
board = pyfirmata.Arduino(arduino_port)

it = pyfirmata.util.Iterator(board)
it.start()

button1 = board.get_pin('d:2:i')
button2 = board.get_pin('d:5:i')
button3 = board.get_pin('d:7:i')
button4 = board.get_pin('d:10:i')
light = board.get_pin('d:11:o')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
host = '192.168.12.90' if robot_connected else '127.0.0.1'

port = 2222
msg = ''
client.connect((host,port)) #Socket oppkobling 
command_number = 0




def main():
    global imgResult

    cap=None

    if cam_connected:
        cap = cv2.VideoCapture(0)
        cap.set(3, 2040)
        cap.set(4, 1080)

    print("-READY-")

    while True:

        button = [button1.read(), button2.read(), button3.read(), button4.read()]
        if button[0] == None:
            continue
            
        if button[0]:
            handleButtonPush(1, cap)
        if button[1]:
            handleButtonPush(2, cap)
        if button[2]:
            handleButtonPush(3, cap)
        
        if button[3]:
            break
        
        board.pass_time(0.2)
        

def handleButtonPush(button, cap):
    global imgResult

    check = checkForPortions(button)

    if check:

        if cam_connected:
            success, img = cap.read()
            success, img = cap.read()
            imgRS = cv2.resize(img, (1020, 540))
            imgResult = imgRS.copy()
            coordinates = findCircle(imgRS)

            if not coordinates:
                return

            cv2.imshow("Result", imgResult)
            cv2.waitKey(1)
            serverClient(coordinates[0], coordinates[1], button)
            cv2.destroyAllWindows()

    
        else:
            t1, t2 = input("Enter x and y: ").split(" ")
            serverClient(int(t1), int(t2), button)

    else:
        print('We are currently out of this drink. Please select a different option or wait for one of our employees to refill the container.')

def checkForPortions(button):
    
    status = drinksSDK.check_portion(button, 'buttonLink')

    if status:
        return True
    else:
        return False

def findCircle(img):
    global imgResult
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    circle_detection = cv2.HoughCircles(imgBlur, cv2.HOUGH_GRADIENT, 1, 10000)
    if circle_detection is not None:
        detected_circles = np.uint16(np.around(circle_detection))
        for (x, y, r) in detected_circles[0, :]:
            cv2.circle(imgResult, (x, y), r, (0, 255, 0), 5)
            cv2.circle(imgResult, (x, y), 2, (0, 255, 255), 3)
        
            print(f"Find Circle - x: {x}  y: {y}")
            return [y,x]
    else:
        return False

def serverClient(x, y, drink_num):

    light.write(1)
    
    if cam_connected:
        
        if x >= 258:
            xValue = (x-305)*0.068 * -1
            xValue = round(xValue*10, 0)
            xValue = f"{xValue}"[:-2]
        else:
            xValue = (x-305)*0.068 * -1
            xValue = round(xValue*10, 0)
            xValue = f"{xValue}"[:-2]

        if y >= 446:
            yValue = (y-500)*0.0724
            yValue = round(yValue*10, 0)
            yValue = f"{yValue}"[:-2]
        else:
            yValue = (y-500)*0.0724
            yValue = round(yValue*10, 0)
            yValue = f"{yValue}"[:-2]
    else:
        xValue, yValue = str(x), str(y)

    drink_num_str = str(drink_num)
    
    if xValue != "+0" and yValue != "+0":
        

        try:
            client.send(bytes(xValue,'utf-8'))
            print(f"X: {xValue}")
            client.recv(1024)
            client.send(bytes(yValue,'utf-8'))
            print(f"Y: {yValue}")
            client.recv(1024)
            client.send(bytes(drink_num_str,'utf-8'))
            print(f"DRINK: {drink_num_str}")
            client.recv(1024)
        except ConnectionRefusedError as e:
            print(e)
        
        print("ORDER RECEIVED AND FORWARDED TO ROBTENDER")
        print(msg)

        catchResponse(drink_num, xValue, yValue)
        

def catchResponse(drink_num, xValue, yValue):

    print("COMPLETING ORDER..")
    try:
        response = client.recv(1024).decode()
    except KeyboardInterrupt:
        print("Cancled by Keyboard Interrupt")
    
    if response == "COMPLETE":
        customerSDK.add_customer(drink_num, xValue, yValue)
        drinksSDK.decrement_portion(drink_num, "buttonLink")
        print ("CUSTOMER APPENDED TO DATABASE AND DRINK DECREMENTED")
    print("ORDER COMPLETE")
    

    light.write(0)


if __name__ == "__main__":
    main()