import busio
from board import SCL, SDA
import RPi.GPIO as GPIO

i2c = busio.I2C(SCL, SDA)

servo_positions = {'flf':14, 'fll':12, 'fls':9,
                   'rlf':1, 'rll':3, 'rls':5,
                   'rrs':4, 'rrl':7, 'rrf':0,
                   'frs':8, 'frl':11, 'frf':15}

# with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
#     for sName in servo_names:
#         # executor.map(move_servo_angle, (sName, 90,))
#         move_servo_angle(sName, 90)

# threads = []
# for sn in servo_names:
#     t = threading.Thread(target=set_servo_angle, args=(sn, 90))
#     threads.append(t)
#     t.start()
# for t in threads:
#     t.join()