from pca_setup import *
from adafruit_motor import servo as servo
import time
import RPi.GPIO as GPIO
import threading
import concurrent.futures
import numpy as np

# servo_positions = {'flf':14, 'fll':12, 'fls':9,
#                    'rlf':1, 'rll':3, 'rls':5,
#                    'rrs':4, 'rrl':7, 'rrf':0,
#                    'frs':8, 'frl':11, 'frf':15}

servo_names=['frf', 'frl', 'frs',
             'flf', 'fll', 'fls',
             'rlf', 'rll', 'rls',
             'rrf', 'rrl', 'rrs']

class SparkyBUBU(object):
    def __init__(self):
        self.pca = pca()
        self.servo_names=servo_names
        self.front_right = servo_names[:3]
        self.front_left = servo_names[3:6]
        self.rear_left = servo_names[6:9]
        self.rear_right = servo_names[9:]
        self.four_legs = [self.front_right, self.front_left, self.rear_left, self.rear_right]
        self.shoulders = [leg[-1] for leg in self.four_legs]
        self.arms = [leg[1] for leg in self.four_legs]
        self.elbows = [leg[0] for leg in self.four_legs]
        self.inverse_joints = ['frf', 'frl', 'frs', 'rls', 'rrf', 'rrl']
        self.normal_joints = [n for n in self.servo_names if n not in self.inverse_joints]
        self.servo_positions = {'flf':14, 'fll':12, 'fls':9,
                        'rlf':1, 'rll':3, 'rls':5,
                        'rrs':4, 'rrl':7, 'rrf':0,
                        'frs':8, 'frl':11, 'frf':15}
        # init with 90 and updated once servos turn on
        self.servo_angles = {'frf':90, 'frl':90, 'frs':90,
                    'flf':90, 'fll':90, 'fls':90,
                    'rlf':90, 'rll':90, 'rls':90,
                    'rrf':90, 'rrl':90, 'rrs':90}
        # needs to be calibrated to have tuple values
        # self.servo_limits = {'frf':90, 'frl':90, 'frs':90,
        #             'flf':90, 'fll':90, 'fls':90,
        #             'rlf':90, 'rll':90, 'rls':90,
        #             'rrf':90, 'rrl':90, 'rrs':90}

    def update_servo_angle(self, sn, a):
        self.servo_angles[sn] = a
            

    def get_servo_angle(self, sn):
        return self.servo_angles[sn]

    def __test_limit(self, sn, a):
        side = 1
        if sn in self.inverse_joints:
            side = -1
        if (a==0 or a==180):
            if side == -1:
                a = 180 - a
        else:
            a = (a * side + 180) % 180
        # checking for limits
        if a<10:
            a = 10
        if a >170:
            a = 170
        return a

    def set_servo_angle(self, sn, a):
        a = self.__test_limit(sn, a)
        active_servo = servo.Servo(self.pca.channels[self.servo_positions[sn]])
        active_servo.angle = a
        self.update_servo_angle(sn,a)
        print("LOG | Servo  " + sn + " (:" + str(self.servo_positions[sn]) + ") at " + str(a) + " degrees")

    def set_servos_angle(self, sns, a):
        for sn in sns:
            self.set_servo_angle(sn, a)

    def move_servo_angle(self, sn, a, interval): #interval in seconds
        a = self.__test_limit(sn, a)
        active_servo = servo.Servo(self.pca.channels[self.servo_positions[sn]])
        cur_angle = self.get_servo_angle(sn)
        if a < cur_angle:
            for angle in np.arange(cur_angle, a-0.1, -0.1):
                active_servo.angle = angle
                self.update_servo_angle(sn,angle)
                time.sleep(interval)
        elif a > cur_angle:
            for angle in np.arange(cur_angle, a+0.1, 0.1):
                active_servo.angle = angle
                self.update_servo_angle(sn,angle)
                time.sleep(interval)
        print("LOG | Servo  " + sn + " (:" + str(self.servo_positions[sn]) + ") at " + str(a) + " degrees")

    # def move_servos_angle(self, sns, a):
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    #         for sName in sns:
    #             executor.submit(self.move_servo_angle, sn=sName, a=a, interval = 0.001)
    #         # executor.shutdown()

    def move_servos_angle(self, sns, a, interval=0.01):
        threads = []
        for sn in sns:
            t = threading.Thread(target=self.move_servo_angle, args=(sn, a, interval))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()






# below functions should take in a robot object



def crouch(robot):
    sns = [s for s in robot.servo_names]
    robot.move_servos_angle(sns, 75)

def sit(robot):
    sns = [s for s in robot.servo_names]
    robot.move_servos_angle(sns, 90)
        

def standup_routine_1(robot):
    bk = input("press enter to begin: ")
    
    for sname in ['flf', 'frf']:
        robot.set_servo_angle(sname, 150)
    for sname in ['rlf', 'rrf']:
        robot.set_servo_angle(sname, 110)
        
    bk = input("press enter...")

    robot.set_servos_angle(['rlf', 'rrf'], 90)

    bk = input("press enter...")

    robot.set_servos_angle(['rll','rrl'], 140)
    robot.set_servos_angle(['rlf','rrf'], 70)

    bk = input("press enter...")

    robot.set_servos_angle(['fll','frl'], 140)
    robot.set_servos_angle(['flf','frf'], 70)

    bk = input('press enter...')

    robot.set_servos_angle(robot.arms, 120)
    robot.set_servos_angle(robot.elbows, 120)
    
def shake_1(robot):
    for sname in robot.shoulders:
        robot.set_servo_angle(sname, 100)
    time.sleep(1)
    for sname in robot.shoulders:
        robot.set_servo_angle(sname, 90)
    time.sleep(1)
    for sname in ['fls','rls']:
        robot.set_servo_angle(sname, 110)
    for sname in ['frs','rrs']:
        robot.set_servo_angle(sname, 70)
    time.sleep(1)
    for sname in ['fls','rls']:
        robot.set_servo_angle(sname, 70)
    for sname in ['frs','rrs']:
        robot.set_servo_angle(sname, 110)
    time.sleep(1)
    for sname in ['fls','rls']:
        robot.set_servo_angle(sname, 90)
    for sname in ['frs','rrs']:
        robot.set_servo_angle(sname, 90)
    brk = input("press enter....")
    robot.set_servos_angle(['fls','rrs'], 80)
    robot.set_servos_angle(['frs','rls'], 100)
    time.sleep(1)
    robot.set_servo_angle('fll', 80)
    robot.set_servo_angle('flf', 90)
    brk = input('press enter...')
    robot.move_servo_angle('fll', 70, 0.005)
    robot.move_servo_angle('fll', 110, 0.005)
    robot.move_servo_angle('fll', 90, 0.005)
    print()
    print(robot.servo_angles)