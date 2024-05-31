# RT1 First Assignment 

## Installing and Running
To run this code, python 3 must be installed, as well as some libraries (pypybox2d, pygame, time, threading). Once all the libraries are installed, clone this github repository using the command below.
```bash
$ git clone https://github.com/OuassimMilous/RT1
```
Now to run the code, in the robot-sim directory, 

```bash
$ python3 run.py assignment.py
```
This should successfully open a new window for the simulator, and the simulator should collect all the boxes to the center.



## The Algorithm Explained:

Start:

- Initialize the robot and constants.
- write all the functions
- set the first seen token as our goal

Main Loop:
- Loop until all the tokens are together.

- Check if Robot is Already Grabbing a Token:

- If it isn't:

 - Find the closest free token.
 - If a free token is found, go and grab it.
 - If no free tokens are found:
  - Check if all tokens are in the goal If yes, break the loop. If not, turn around until you find more tokens.

- If it is:
  - Find the closest goal.
  - If a goal is found, go release the token.
  - If no goal is found, turn around until you find one.
End loop.

if the loop ends it means all the tokens are in the goal aand the program ends.

## The Pseudo Code:

```

# Function to set linear velocity
function drive(speed, seconds):
    Set power of left and right motors to 'speed'
    Sleep for 'seconds'
    Set power of left and right motors to 0

# Function to set angular velocity
function turn(speed, seconds):
    Set power of left motor to 'speed'
    Set power of right motor to '-speed'
    Sleep for 'seconds'
    Set power of left and right motors to 0

# Function for the robot to follow directions to a certain direction
function follow_directions(dist, rot_y):
    If rot_y is less than -a_th:
        Turn left with a speed of -10 for 0.1 seconds
    Else if rot_y is greater than a_th:
        Turn right with a speed of 10 for 0.1 seconds
    
    If dist is greater than or equal to close:
        Drive forward with a speed of 60 for 0.1 seconds
    If dist is less than close and greater than d_th:
        Drive forward with a speed of 15 for 0.1 seconds

# Function to get directions to a set token
function get_the_way(code):
    Set initial dist to 1000
    For each token seen by the robot:
        If token.dist is less than dist and token.info.code is equal to code:
            Update dist to token.dist
            Set rot_y to token.rot_y
    
    If dist is still 1000:
        Return -1, -1
    Else:
        Return dist, rot_y

# Function for the robot to go grab or release a token
function go_get_it(code, to_get):
    Set dist, rot_y to the result of get_the_way(code)
    
    While (dist is greater than d_th and to_get) or (dist is greater than d_th_goal and not to_get):
        Update code by scanning for tokens (not to_get)
        Update dist, rot_y to the result of get_the_way(code)
        
        If dist is -1 and rot_y is -1:
            Print "we lost the way! let's look for it again"
            For i in range 5:
                Turn right with a speed of 5 for 0.05 seconds
                Update dist, rot_y to the result of get_the_way(code)
                If dist is not -1, break
            For i in range 5:
                Turn left with a speed of 5 for 0.05 seconds
                Update dist, rot_y to the result of get_the_way(code)
                If dist is not -1, break
        Else:
            Call follow_directions(dist, rot_y)

    If dist is not -1:
        If to_get is true:
            Grab the token
            Turn right with a speed of 2 for 1 second
            Append code to the goal list
            Return True
        Else:
            Release the token
            Drive backward with a speed of 15 for 1 second
            Return False

# Function to scan the area for tokens
function scan(type):
    Set dist to 1000
    For each token seen by the robot:
        If token.info.code is not in unique_markers:
            Append token.info.code to unique_markers
        
        If type is true:
            If token.info.code is in goal and token.dist is greater than d_th:
                Update dist to token.dist
                Set code to token.info.code
        Else:
            If token.info.code is not in goal and token.dist is less than dist:
                Update dist to token.dist
                Set code to token.info.code
    
    If dist is still 1000:
        Return -1
    Else:
        Return code

# Main function
function main():
    Set grabbing to False
    Append the result of scanning for goal tokens (False) to the goal list

    While True:
        If grabbing is False:
            Update code by scanning for free tokens (False)
            If code is not -1:
                Set grabbing to the result of go_get_it(code, True)
            Else:
                If the length of goal is equal to the length of unique_markers:
                    Break the loop
                If code is -1:
                    Turn right with a speed of 10 for 0.5 seconds
        Else:
            Update code by scanning for goal tokens (True)
            If code is not -1:
                Set grabbing to the result of go_get_it(code, False)
            Else:
                If code is -1:
                    Turn right with a speed of 10 for 0.5 seconds

    Print "Mission Accomplished"

# Run the main function
Call main()

```



## Possible Improvements

- we can get the robot to put the tokens in the middle instead of putting them next to the first token it sees.
- sometimes for long distances the robot fails to see the target and loses its direction. my solution was to turn around again until it finds it, but I'm sure it could be better optimized.




