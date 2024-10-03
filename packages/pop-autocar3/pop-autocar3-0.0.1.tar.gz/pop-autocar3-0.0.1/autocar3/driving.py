import math
import numpy as np

# from .config import IP, GROUP, __version__
# from .Util import ICAN

from config import IP, GROUP, __version__
from Util import ICAN

class Driving(ICAN):
    ID_DRIVING = 0x010
    THROTTLE_0POINT = 100
    WHEEL_STOP = 0
    WHEEL_FORWARD = 1
    WHEEL_BACKWARD = 2
    STEER_ID = 0x013
    STEER_CENTER = 90

    def __init__(self, ip=IP, group=GROUP):
        super().__init__(ip, group)
        self.__ican = self.ican
        self.__steering = 0.0
        self.__throttle = 0
        self.stop()

    def __transfer(self, id, payload, is_extended=False):
        self.__ican.write(
            id, payload, is_extended
        )

    def move(self, throttle=None, cm=None, direction=None):
        if throttle is not None:
            self.__throttle = throttle
            
        if self.__moving != direction:
            self.__moving = direction
        
        if self.__moving == self.WHEEL_FORWARD:
            if self.__throttle < 0:
                self.__throttle *= -1
        elif self.__moving == self.WHEEL_BACKWARD:
            if self.__throttle > 0:
                self.__throttle *= -1
        
        if cm is None:
            payload = [100+self.__throttle, 0]
        else:
            payload = [100+self.__throttle, cm]
        self.__transfer(self.ID_DRIVING, payload)

    def stop(self):
        self.__throttle = 0
        self.__moving = self.WHEEL_STOP
        self.__transfer(self.ID_DRIVING, [100+self.__throttle,0])

    @property
    def throttle(self):
        return self.__throttle

    @throttle.setter
    def throttle(self, throttle):
        if 0 <= throttle <= 100:
            if self.__moving == self.WHEEL_BACKWARD:
                self.__throttle = throttle * -1
            else:
                self.__throttle = throttle
        
            if self.__moving is not self.WHEEL_STOP:
                self.move()
        else:
            print("Warning : This value is out of range 0 to 100")

    @property
    def steering(self):
        return self.__steering

    @steering.setter
    def steering(self, value):
        if value > 1.0 or value < -1.0:
            print("Warning : This value is out of range -1.0 to 1.0")
            if value > 1.0:
                value = 1.0
            elif value < -1.0:
                value = -1.0
        self.__steering = value 
        data = self.STEER_CENTER + int(value*35)
        self.__transfer(self.STEER_ID,[data&0xff,(data>>8)&0xff])

    def forward(self, throttle=None):
        self.move(throttle,0,self.WHEEL_FORWARD)

    def backward(self, throttle=None):
        self.move(throttle,0,self.WHEEL_BACKWARD)
