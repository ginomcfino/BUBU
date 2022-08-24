import busio
from board import SCL, SDA
import RPi.GPIO as GPIO

i2c = busio.I2C(SCL, SDA)

servo_positions = {'flf':14, 'fll':12, 'fls':9,
                   'rlf':1, 'rll':3, 'rls':5,
                   'rrs':4, 'rrl':7, 'rrf':0,
                   'frs':8, 'frl':11, 'frf':15}

servoPIN = 