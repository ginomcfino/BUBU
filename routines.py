from sparkybubu import SparkyBUBU
import time


# servo_names=['frf', 'frl', 'frs',
#              'flf', 'fll', 'fls',
#              'rlf', 'rll', 'rls',
#              'rrf', 'rrl', 'rrs']

# self.servo_angles = {'frf':90, 'frl':90, 'frs':90,
#                     'flf':90, 'fll':90, 'fls':90,
#                     'rlf':90, 'rll':90, 'rls':90,
#                     'rrf':90, 'rrl':90, 'rrs':90}

def uptown_spot(robot):
    stand_angles = {'frf':30, 'frl':150, 'frs':75,
                    'flf':30, 'fll':150, 'fls':75,
                    'rlf':30, 'rll':150, 'rls':75,
                    'rrf':30, 'rrl':150, 'rrs':75}
    robot.move_servos(stand_angles, 0.001)


# below functions should take in a robot object

def crouch(robot):
    # sns = [s for s in robot.servo_names]
    # robot.move_servos_angle(sns, 75)
    stand_angles = {'frf':30, 'frl':150, 'frs':75,
                    'flf':30, 'fll':150, 'fls':75,
                    'rlf':30, 'rll':150, 'rls':75,
                    'rrf':30, 'rrl':150, 'rrs':75}
    robot.move_servos(stand_angles, 0.001)

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