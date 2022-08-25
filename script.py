#!/home/pi/BUBU/venv/bin/python3 -u

from sparkybubu import *

#todo: make SparkyBUBU class for Object-Oriented Control!
#todo: make walk functions (combine the move_servo functions into some kind of IK)


if __name__=="__main__":
    # initialize the robot
    bubu = SparkyBUBU()

    print("NOW beginning testing loop: ")
    command = input("available commands: \ncrouch | sit | stand1 | shake1 | testservo \n")
    while not (command == "quit" or command == "exit"):
        if command == "crouch": #crouch
            crouch(bubu)
            print("BUBU crouching")
        elif command == "sit" or command == "SIT": #sit
            sit(bubu)
            print("BUBU sitting")
        elif command == "stand1":
            standup_routine_1(bubu)
        elif command == "shake1":
            shake_1(bubu)
        elif command == "testservo":
            sn = input("which servo? ")
            a = input("to what angle? ")
            bubu.set_servo_angle(sn, int(a))
        command = input("available commands: \ncrouch | sit | stand1 | shake1 \n")
        
        
        
        
        
