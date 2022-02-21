#!/home/pi/spotmicroai/venv/bin/python3 -u

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo as servo
from pick import pick
import time
from math import pi
import RPi.GPIO as GPIO
from spot_micro_kinematics_python.spot_micro_stick_figure import SpotMicroStickFigure

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config


log = Logger().setup_logger('Powering up SPARKY!')
log.info('setup')


pca=None
pca9685_address = 0x40
pca9685_reference_clock_speed = int(Config().get(
    'motion_controller[*].boards[*].pca9685_1[*].reference_clock_speed | [0] | [0] | [0]'))
pca9685_frequency = int(
    Config().get('motion_controller[*].boards[*].pca9685_1[*].frequency | [0] | [0] | [0]'))


gpio_port = Config().get(Config.ABORT_CONTROLLER_GPIO_PORT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_port, GPIO.OUT)
GPIO.output(gpio_port, False)
time.sleep(1)

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c_bus=i2c, address=pca9685_address, reference_clock_speed=pca9685_reference_clock_speed)
pca.frequency = pca9685_frequency

# Some References that might be useful for coding motion of servos
#order: 
# rear_left: 8, 9, 10(shoulder, leg, feet), = 0, 1, 2
# rear_right: 12, 13, 14                    = 3, 4, 5
# front_left: 4, 5, 6                       = 6, 7, 8
# front_right: 0, 1, 2                      = 9, 10, 11
# servos_pos_help is meant to only help see where the above servo positions are found and nothing else
# servos_pos_help2 is meant to only help see where the above servo positions are found and nothing else
servo_names = {"frf":0, "frl": 1, "frs": 2,
               "flf":4, "fll": 5, "fls": 6,
               "rlf":8, "rll": 9, "rls": 10,
               "rrf":12, "rrl":13, "rrs": 14}
servo_angles = {"frf":90, "frl": 90, "frs": 90,
               "flf":90, "fll": 90, "fls": 90,
               "rlf":90, "rll": 90, "rls": 90,
               "rrf":90, "rrl": 90, "rrs": 90}
servos = [(8,90),(9,90),(10,90),(12,90),(13,90),(14,90),(4,90),(5,90),(6,90),(0,90),(1,90),(2,90)]
servos_pos_help     = [  8,   9, 10,  12, 13,  14,   4,   5,  6,  0,   1,   2]
servos_pos_help2    = [  0,   1,  2,   3,  4,   5,   6,   7,  8,  9,  10, 11]
rest_angles         = [ 75, 100,  0, 105, 80, 180, 105, 100, 0, 75, 80, 180]
stand_angles        = [ 75,  90, 90, 105, 90,  90, 105, 90, 90, 75, 90,  90]
front_shoulders = [4, 0]
back_shoulders = [8,12]

sparky = SpotMicroStickFigure()

def set_servo_angle(sn, a):
    if a <=10:
        a = 10
    if a>=170:
        a = 170
    active_servo = servo.Servo(pca.channels[sn])
    active_servo.set_pulse_width_range(min_pulse=500, max_pulse=2500)
    active_servo.angle=a
    set_servo_angle(sn, a)

def update_servo_angle(sn, a):
    servo_angles[sn] = a

def adj_servo_angle(s, a):
    active_servo = servo.servo(pca.channels[s])        

def squat(a):
    set_servo_angle(1, servos[1][1]+a)
    set_servo_angle(2, servos[2][1]-a)
    set_servo_angle(7, servos[7][1]+a)
    set_servo_angle(8, servos[8][1]-a)
    set_servo_angle(4, servos[4][1]-a)
    set_servo_angle(5, servos[5][1]+a)
    set_servo_angle(10, servos[10][1]-a)
    set_servo_angle(11, servos[11][1]+a)

def unsquat(a):
    set_servo_angle(1, servos[1][1]-a)
    set_servo_angle(2, servos[2][1]+a)
    set_servo_angle(7, servos[7][1]-a)
    set_servo_angle(8, servos[8][1]+a)
    set_servo_angle(4, servos[4][1]+a)
    set_servo_angle(5, servos[5][1]-a)
    set_servo_angle(10, servos[10][1]+a)
    set_servo_angle(11, servos[11][1]-a)

def crowch(a):
    set_servo_angle(1, servos[1][1]+a)
    set_servo_angle(2, servos[2][1]-(a*2))
    set_servo_angle(7, servos[7][1]+a)
    set_servo_angle(8, servos[8][1]-(a*2))
    set_servo_angle(4, servos[4][1]-a)
    set_servo_angle(5, servos[5][1]+(a*2))
    set_servo_angle(10, servos[10][1]-a)
    set_servo_angle(11, servos[11][1]+(a*2))

def uncrowch(a):
    set_servo_angle(1, servos[1][1]-a)
    set_servo_angle(2, servos[2][1]+(a*2))
    set_servo_angle(7, servos[7][1]-a)
    set_servo_angle(8, servos[8][1]+(a*2))
    set_servo_angle(4, servos[4][1]+a)
    set_servo_angle(5, servos[5][1]-(a*2))
    set_servo_angle(10, servos[10][1]+a)
    set_servo_angle(11, servos[11][1]-(a*2))
    
def rest_position():
    for x in range(len(servos)):
        set_servo_angle(x, rest_angles[x])
    time.sleep(0.1)

def sit_back(a):
    set_servo_angle(1, servos[1][1]-a)
    set_servo_angle(2, servos[2][1]-(0.5*a))
    set_servo_angle(4, servos[4][1]+a)
    set_servo_angle(5, servos[5][1]+(0.5*a))

def stand_straight():
    for x in range(len(servos)):
        set_servo_angle(x, stand_angles[x])
    time.sleep(0.1)

def roll_left(a):
    set_servo_angle(6, servos[6][1]+a)
    set_servo_angle(9, servos[9][1]+a)
    set_servo_angle(0, servos[0][1]-a)
    set_servo_angle(3, servos[3][1]-a)

def roll_right(a):
    set_servo_angle(6, servos[6][1]-a)
    set_servo_angle(9, servos[9][1]-a)
    set_servo_angle(0, servos[0][1]+a)
    set_servo_angle(3, servos[3][1]+a)

def set_body():
    sparky.set_body_angles(theta=10*pi/180)

def move_feet_back(side, deg):
    if side == 0:
        cur_angle = servo_angles["flf"]
        set_servo_angle("flf", cur_angle)
        set_servo_angle("rlf", cur_angle)
        for i in range(deg):
            cur_angle+=0.5
            set_servo_angle("flf", cur_angle)
            set_servo_angle("rlf", cur_angle)
            time.sleep(0.1)
    else:
        cur_angle = servo_angles["frf"]
        set_servo_angle("frf", cur_angle)
        set_servo_angle("rrf", cur_angle)
        for i in range(deg):
            cur_angl-=0.5
            set_servo_angle("frf", cur_angle)
            set_servo_angle("rrf", cur_angle)
            time.sleep(0.1)


if __name__=="__main__":
    #stand_straight()

    #initialize to 90 degree rest mode
    for joint in servo_names.keys():
        set_servo_angle(joint, 90)
    time.sleep(5)

    #stand up
    move_feet_back(0, 20)
    move_feet_back(1, 20)

    while(True):
        action= input("What would you like to do? ")
        if action=="sit":
            rest_position()
        elif action=="stand":
            stand_straight()
        elif action=="sit back":
            try:
                while(True):
                    sit_back(.2)
                    time.sleep(.01)
            except KeyboardInterrupt:
                print("stopped")
                pass
        elif action=="roll left":
            try:
                while(True):
                    roll_left(.2)
                    time.sleep(.01)
            except KeyboardInterrupt:
                print("stopped")
                pass
        elif action=="roll right":
            try:
                while(True):
                    roll_right(.2)
                    time.sleep(.01)
            except KeyboardInterrupt:
                print("stopped")
                pass
        elif action=="squat":
            while(True):
                itrpt = input("type stop to STOP: ")
                if itrpt=="stop":
                    break
                else:
                    squat(5)
                    time.sleep(.1)
        elif action=="unsquat":
            while(True):
                itrpt = input("type stop to STOP: ")
                if itrpt=="stop":
                    break
                else:
                    unsquat(5)
                    time.sleep(.1)
        elif action=="crowch":
            while(True):
                itrpt = input("type stop to STOP: ")
                if itrpt=="stop":
                    break
                else:
                    crowch(2)
                    time.sleep(.1)
        elif action=="uncrowch":
            while(True):
                itrpt = input("type stop to STOP: ")
                if itrpt=="stop":
                    break
                else:
                    uncrowch(2)
                    time.sleep(.1)
        else:
            print("terminating...")
            break
        # time.sleep(5)
    # while(True):
    #     roll_left(10)
    #     time.sleep(2)
    #     roll_right(10)
    #     time.sleep(2)
    #     roll_right(10)
    #     time.sleep(2)
    #     roll_left(10)
    #     time.sleep(2)
    # try:
    #     set_body()
    #     while(True):
    #         rest_position()
    #         print(sparky.get_leg_angles())
    #         time.sleep(5)
    #         stand_straight()
    #         print(sparky.get_leg_angles())
    #         time.sleep(5)
    #         roll_left()
    #         time.sleep(5)
    # except:
    #     log.error("trouble connecting to the servos")
