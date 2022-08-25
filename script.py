#!/home/pi/BUBU/venv/bin/python3 -u

from sparkybubu import *

#todo: make SparkyBUBU class for Object-Oriented Control!
#todo: make walk functions (combine the move_servo functions into some kind of IK)


if __name__=="__main__":
    print("NOW beginning testing loop: ")
    command = input("available commands: \ncrouch | sit | stand1 | shake1 \n")
    while not (command == "quit" or command == "exit"):
        if command == "crouch": #crouch
            crouch()
            print("BUBU crouching")
        elif command == "sit" or command == "SIT": #sit
            sit()
            print("BUBU sitting")
        elif command == "stand1":
            standup_routine_1()
        elif command == "shake1":
            shake_1()
        command = input("available commands: \ncrouch | sit | stand1 | shake1 \n")
        
        
        
        
        
