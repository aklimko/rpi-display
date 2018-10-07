import threading
import time

import RPi.GPIO as GPIO

import configuration


class Buttons:
    def __init__(self, device, mode):
        self.left = 17
        self.right = 26
        self._setup_gpio()
        self._buttons_cfg = configuration.ButtonsCfg()
        self._device = device
        self._mode = mode

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left, GPIO.IN)
        GPIO.setup(self.right, GPIO.IN)
        GPIO.add_event_detect(self.left, GPIO.RISING, bouncetime=250)
        GPIO.add_event_detect(self.right, GPIO.RISING, bouncetime=250)

    def setup_listener(self):
        threading.Thread(target=self._listener, daemon=True).start()

    def _listener(self):
        while True:
            if GPIO.event_detected(self.left):

                time.sleep(self._buttons_cfg.get_wait_time_after_click())
            elif GPIO.event_detected(self.right):
                self._mode.switch()
                self._device.clear()
                time.sleep(self._buttons_cfg.get_wait_time_after_click())
            else:
                time.sleep(0.2)
