import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685


def pca():
    pca=None

    pca9685_address = 0x40
    print("pca address: " + str(pca9685_address)) #0x40

    pca9685_reference_clock_speed = 25000000
    print("clock speed: " + str(pca9685_reference_clock_speed)) #25,000,000 ie 25mHz

    pca9685_frequency = 50
    print("frequency: " + str(pca9685_frequency)) #50

    #gpio_port = Config().get(Config.ABORT_CONTROLLER_GPIO_PORT)
    #print("abort controller: " + str(gpio_port)) # 17

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(gpio_port, GPIO.OUT)
    #GPIO.output(gpio_port, False)
    #time.sleep(1)
    # GPIO is completely unused

    i2c = busio.I2C(SCL, SDA)

    pca = PCA9685(i2c_bus=i2c, address=pca9685_address, reference_clock_speed=pca9685_reference_clock_speed)
    pca.frequency = pca9685_frequency

    print("SETUP Complete.")
    
    return pca
