        
import RPi.GPIO as GPIO
import pigpio
import time

from threading import Thread
constrain = lambda x, min_, max_: min_ if x < min_ else (max_ if x > max_ else x) 
class WaterGun(Thread):
    def __init__(self, pan_pin = 15, tilt_pin = 18, shoot_pin = 14, center = (1500, 1500), max_on_time = 5):
        super().__init__()
        #self.daemon = True
        self.__alive = True
        self.started = False
        
        self.__last_on = time.time()
        self.__last_on_duration = 0 # Remember On-time to allow solenoid to cool  appropriately 
        self.__last_off = time.time()
        self.gpio = pigpio.pi()
        self.gpio.set_mode(pan_pin, pigpio.OUTPUT)
        self.gpio.set_mode(tilt_pin, pigpio.OUTPUT)
        self.gpio.set_mode(shoot_pin, pigpio.OUTPUT)
        
        self.gpio.set_PWM_frequency(pan_pin, 50)
        self.gpio.set_PWM_frequency(tilt_pin, 50)
        
        self.gpio.set_servo_pulsewidth(pan_pin, center[0])
        self.gpio.set_servo_pulsewidth(tilt_pin, center[1])
        self.gpio.write(shoot_pin, 0)
        
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.shoot_pin = shoot_pin
        self.__center = center
        self.max_on_time = max_on_time
        self.shot_clock = max_on_time
        
        self.pan = 0
        self.tilt = 0
        
    @property
    def pan(self):
        return self._pan
    
    @pan.setter
    def pan(self, value):
        self._pan = constrain(value, 0, 100)
        value = 500 + int(self._pan * 20)
        self.gpio.set_servo_pulsewidth(self.pan_pin, value)
        
    @property
    def tilt(self):
        return self._tilt
    
    @tilt.setter
    def tilt(self, value):
        self._tilt = constrain(value, 0, 100)
        value = 1000 + int(self._tilt * 10)
        self.gpio.set_servo_pulsewidth(self.tilt_pin, value)
    
    def center(self):
        pass
    
    def run(self):
        self.started = True
        try:
            while self.__alive:
                if time.time() - self.__last_on >= self.max_on_time - 1:
                    self.stop()
                if time.time() - self.__last_on >= self.shot_clock - 1:
                    self.shot_clock = self.max_on_time
                    self.stop()
        finally:
            self.stop()
            self.close()
    
    def shoot(self, duration=-1):
        if(self.started):
            if self.__last_off > self.__last_on:
                if time.time() - self.__last_off < self.__last_on_duration * 2:
                    print("To Soon Allowing solenoid to cool. Shot Skipped")
                else:
                    self.__last_on = time.time()
                    if duration != -1:
                        self.shot_clock = duration
                    self.gpio.write(self.shoot_pin, 1)
        
    def stop(self):
        if self.__last_off < self.__last_on:
            self.__last_on_duration = self.__last_on - self.__last_off 
            self.__last_off = time.time()
        self.gpio.write(self.shoot_pin, 0)

    def close(self):
        self.gpio.set_PWM_dutycycle(self.pan_pin, 0)
        self.gpio.set_PWM_dutycycle(self.tilt_pin, 0)
        
        self.gpio.set_PWM_frequency(self.pan_pin, 0)
        self.gpio.set_PWM_frequency(self.tilt_pin, 0)
        self.gpio.write(self.shoot_pin, 0)
        self.__alive = False

if __name__ == "__main__":
    import time

    gun = WaterGun(max_on_time = 3)
    gun.start()
    while True:
        for i in [0, 50, 100]:
            gun.pan = i
            time.sleep(1)
            for j in [0, 50, 70]:
                gun.tilt = j
                time.sleep(.5)
                gun.shoot()
                time.sleep(1)
                gun.stop()
                time.sleep(.5)