from __future__ import print_function
from math import dist
from pyexpat.errors import codes
from shutil import move
from termios import OFDEL
import time
import token
import sys
import os
import signal

from xml.etree.ElementTree import tostring
from sr.robot import *


def send_signal_to_run():
    # Read the PID of run.py from the file
    with open('run_pid.txt', 'r') as f:
        run_pid = int(f.read().strip())

    # Send a signal to run.py to shut it down
    os.kill(run_pid, signal.SIGTERM)



R = Robot()


a_th = 2.0
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""

d_th_goal = 0.55
""" float: Threshold for the control of the orientation for the goal location"""

close = 0.6
""" float: a constant to know when a token is close to the robot"""

goal = []
""" array: a list of the tokens already put in the goal location"""

unique_markers = []
""" array: a list of all the tokens"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def follow_directions(dist,rot_y):
    """
    Function for the robot to go to a certaion direction

    Args: dist (int): linear distance
          rot_y (int): angle
    """
    # set the correct angle
    if (-a_th > rot_y ):
        turn(-10,0.1)
    elif(rot_y > a_th):
        turn(10,0.1)
    # go fast when we are far
    if(dist>=close):
        drive(2000,0.1)
    # approach slowly when we are close
    if(dist<close and dist>d_th):
        drive(2000,0.1)

def get_the_way(code):
    """
    Function for the robot to get the directions to a set token

    Args: code (int): id of the targeted token
          
    return: dist (int): the linear distance towards the robot
            rot_y (int): the angle to the destination
    """
    
    #set the distance to a 1000 than we try to update it with the actual value. if it stays the same we know we failed to find the target
    dist = 1000
    #we scan for tokens
    for token in R.see():

        #here we check if we found our target, if we do so we update the data to be returned
        if token.dist < dist and token.info.code == code:
            dist = token.dist
            rot_y = token.rot_y
    #if we fail to find the target we return -1
    if dist == 1000:
        return -1, -1
    #else, we return the values
    else:
        return dist, rot_y

def go_get_it(code, to_get):
    """
    Function for the robot to go grab the token or to release it when the goal is reacher

    Args:   code (int): id of the targeted token
            to_get (bool):      True = we want to grab a token
                                False = we want to drop it in the goal
          
    return: grabbing (bool):    wether or not the robot is grabbing a token
    """
    #we get the initial directoins to the target
    dist,rot_y = get_the_way(code)

    #the code keeps on executing as long as the threashhold is not reached yet
    while ((dist > d_th and to_get) or (dist > d_th_goal and not to_get)):
        
        #we keep on updating our token lists
        code = scan(not to_get)

        #get the directoins to the target
        dist,rot_y = get_the_way(code)

        #in case we lose our way, we turn right and back to look for it again
        if(dist == -1 and rot_y == -1):
            print("we lost the way! lets look for it again")
            for i in range(5):
                turn(5,0.05)
                dist,rot_y = get_the_way(code)
                if dist != -1:
                    break
            for i in range(5):
                turn(-5,0.05)
                dist,rot_y = get_the_way(code)
                if dist != -1:
                    break

        else:
            #in case we're on the right way, we go to the target
            follow_directions(dist, rot_y)

    #if we reach our distination, we grab or release the token as specified
    if(dist!=-1):
        if(to_get):
            if dist < close:
                #we grab the token and update our list
                R.release()
                R.grab() 
                turn(2,1)
                goal.append(code)    
                return True
        else:
            #we release the token and go back a bit to not push boxes
            R.release()
            drive(-50,1)
            return False
        
          

def scan(type):
    """
    Function to scan the area to look for tokens
    Args:   
            type (bool):    True = we scan for free tokens
                            False = we scan for tokens in the goal
          
    return: code (int):     id of the closest targeted token
    """

    #set the distance to a 1000 than we try to update it with the actual value. if it stays the same we know we failed to find the target
    dist = 1000
    #we scan for tokens
    for token in R.see():

        #we make sure to include all unique tokens in our list unique_markers 
        if token.info.code not in unique_markers:
            unique_markers.append(token.info.code)

        if(type):
        #if we are looking for tokens in the goal area we choose them then compare how close they are to the next goal token
             if (token.info.code in goal) and (token.dist>d_th):
                dist = token.dist
                code = token.info.code
        else:
        #if we are looking for free tokens we choose them then compare how close they are to the next free token

            if( not (token.info.code in goal) and (token.dist < dist)):
                dist = token.dist
                code = token.info.code
    #if we fail to find the target we return -1
    if dist == 1000:
        return -1
    #else, we return the code to the closest target
    else:
        return code


# here goes the code
def main():

    #we know our robot isnt grabbing anything when we start
    grabbing = False
    
    # so we set the closest token we intially see as a goal
    goal.append(scan(False))

    # here our code will run untill we complete our mission
    while 1:
        if not grabbing:
            code = scan(False)
            if code != -1:
                grabbing = go_get_it(code, True)
            else:
                if len(goal) == len(unique_markers):
                    break
                if code == -1:
                    turn(-30, 0.1)
        else:
            code = scan(True)
            if code != -1:
                grabbing = go_get_it(code, False)
            else:
                if code == -1:
                    turn(-30, 0.1)

    #if we are out of the loop it means we made it!
    print("Mission Accomplished")
    send_signal_to_run()
    sys.exit()  
main()