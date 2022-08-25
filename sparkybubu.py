from pca_setup import *
from adafruit_motor import servo as servo
import time
from math import pi
import RPi.GPIO as GPIO
import threading
import concurrent.futures
from utilities.log import Logger
from utilities.config import Config
import numpy as np


pca = pca() # initializing the servo hat

servo_names=['frf', 'frl', 'frs',
             'flf', 'fll', 'fls',
             'rlf', 'rll', 'rls',
             'rrf', 'rrl', 'rrs']

front_right = servo_names[:3]
front_left = servo_names[3:6]
rear_left = servo_names[6:9]
rear_right = servo_names[9:]

four_legs = [front_right, front_left, rear_left, rear_right]
shoulders = [leg[-1] for leg in four_legs]
arms = [leg[1] for leg in four_legs]
elbows = [leg[0] for leg in four_legs]
    
inverse_joints = ['frf', 'frl', 'frs', 'rls', 'rrf', 'rrl']
normal_joints = [n for n in servo_names if n not in inverse_joints]


servo_positions = {'flf':14, 'fll':12, 'fls':9,
                   'rlf':1, 'rll':3, 'rls':5,
                   'rrs':4, 'rrl':7, 'rrf':0,
                   'frs':8, 'frl':11, 'frf':15}

# storing the current servo angle, init with 90
servo_angles = {'frf':90, 'frl':90, 'frs':90,
               'flf':90, 'fll':90, 'fls':90,
               'rlf':90, 'rll':90, 'rls':90,
               'rrf':90, 'rrl':90, 'rrs':90}

# needs to be calibrated to have tuple values
servo_limits = {'frf':90, 'frl':90, 'frs':90,
               'flf':90, 'fll':90, 'fls':90,
               'rlf':90, 'rll':90, 'rls':90,
               'rrf':90, 'rrl':90, 'rrs':90}


def set_servo_angle(sn, a):
    side = 1
    if sn in inverse_joints:
        side = -1
    if (a==0 or a==180):
        if side == -1:
            a = 180 - a
    else:
        a = (a * side + 180) % 180
    if a<10:
        a = 10
    if a >170:
        a = 170
    active_servo = servo.Servo(pca.channels[servo_positions[sn]])
    #active_servo.set_pulse_width_range(min_pulse=500, max_pulse=2500)
    active_servo.angle = a
    update_servo_angle(sn,a)
    print("LOG | Servo  " + sn + " (:" + str(servo_positions[sn]) + ") at " + str(a) + " degrees")


def move_servo_angle(sn, a):
    side = 1
    if sn in inverse_joints:
        side = -1
    if (a==0 or a==180):
        if side == -1:
            a = 180 - a
    else:
        a = (a * side + 180) % 180
    if a<10:
        a = 10
    if a >170:
        a = 170
    active_servo = servo.Servo(pca.channels[servo_positions[sn]])
    #active_servo.set_pulse_width_range(min_pulse=500, max_pulse=2500)
    cur_angle = get_servo_angle(sn)
    if a < cur_angle:
        for angle in np.arange(cur_angle, a-0.1, -0.1):
            active_servo.angle = angle
            update_servo_angle(sn,angle)
            time.sleep(0.001)
    elif a > cur_angle:
        for angle in np.arange(cur_angle, a+0.1, 0.1):
            active_servo.angle = angle
            update_servo_angle(sn,angle)
            time.sleep(0.001)
    print("LOG | Servo  " + sn + " (:" + str(servo_positions[sn]) + ") at " + str(a) + " degrees")


def set_servos_angle(sns, a):
    for sn in sns:
        set_servo_angle(sn, a)
    

def update_servo_angle(sn, a):
    servo_angles[sn] = a
        

def get_servo_angle(sn):
    return servo_angles[sn]

def crouch():
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for sName in servo_names:
            executor.submit(move_servo_angle,sn=sName, a=75)

        executor.shutdown()

def sit():
    for sName in servo_positions.keys():
        set_servo_angle(sName, 90)
        

def standup_routine_1():
    bk = input("press enter to begin: ")
    
    for sname in ['flf', 'frf']:
        set_servo_angle(sname, 150)
    for sname in ['rlf', 'rrf']:
        set_servo_angle(sname, 110)
        
    bk = input("press enter...")

    set_servos_angle(arms, 120)
    set_servos_angle(['rlf', 'rrf'], 90)

    bk = input("press enter...")

    set_servos_angle(['rll','rrl'], 140)
    set_servos_angle(['rlf','rrf'], 70)

    bk = input("press enter...")

    set_servos_angle(['fll','frl'], 140)
    set_servos_angle(['flf','frf'], 70)

    bk = input('press enter...')

    set_servos_angle(arms, 120)
    set_servos_angle(elbows, 120)
    
def shake_1():
    for sname in shoulders:
        set_servo_angle(sname, 100)
    time.sleep(1)
    for sname in shoulders:
        set_servo_angle(sname, 90)
    time.sleep(1)
    for sname in ['fls','rls']:
        set_servo_angle(sname, 110)
    for sname in ['frs','rrs']:
        set_servo_angle(sname, 70)
    time.sleep(1)
    for sname in ['fls','rls']:
        set_servo_angle(sname, 70)
    for sname in ['frs','rrs']:
        set_servo_angle(sname, 110)
    time.sleep(1)
    for sname in ['fls','rls']:
        set_servo_angle(sname, 90)
    for sname in ['frs','rrs']:
        set_servo_angle(sname, 90)
    brk = input("press enter....")
    set_servos_angle(['fls','rrs'], 80)
    set_servos_angle(['frs','rls'], 100)
    time.sleep(1)
    set_servo_angle('fll', 80)
    set_servo_angle('flf', 90)
    brk = input('press enter...')
    move_servo_angle('fll', 70)
    move_servo_angle('fll', 110)
    move_servo_angle('fll', 90)
    print()
    print(servo_angles)