import spidev
import RPi.GPIO as GPIO
import time
import tkinter as tk
from threading import Thread


class ButtonEventGroup():
    def __init__(self) -> None:
        # Initialize self.SPI
        
        GPIO.cleanup()
        
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000

        # Define motor and relay pins
        self.Motor_A_1 = 6
        self.Motor_A_2 = 5
        self.Motor_B_1 = 21
        self.Motor_B_2 = 20
        self.Relay_valve = [17, 27]

        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Setup GPIO pins
        GPIO.setup(self.Motor_A_1, GPIO.OUT)
        GPIO.setup(self.Motor_A_2, GPIO.OUT)
        GPIO.setup(self.Motor_B_1, GPIO.OUT)
        GPIO.setup(self.Motor_B_2, GPIO.OUT)
        GPIO.setup(self.Relay_valve, GPIO.OUT)

        # Setup PWM
        self.Motor_A_1_PWM = GPIO.PWM(self.Motor_A_1, 20)
        self.Motor_A_2_PWM = GPIO.PWM(self.Motor_A_2, 20)
        self.Motor_B_1_PWM = GPIO.PWM(self.Motor_B_1, 20)
        self.Motor_B_2_PWM = GPIO.PWM(self.Motor_B_2, 20)

        self.Motor_A_1_PWM.start(0)
        self.Motor_A_2_PWM.start(0)
        self.Motor_B_1_PWM.start(0)
        self.Motor_B_2_PWM.start(0)

        GPIO.output(self.Motor_A_2, GPIO.LOW)
        GPIO.output(self.Motor_B_2, GPIO.LOW)

        # Initialize variables
        self.running = False
        self.stop_all = False
        self.duty_cycle = 100  # Initial duty cycle set to 100%

    def analogRead(self, channel):
        buf = [(1 << 2) | (1 << 1) | (channel & 4) >> 2, (channel & 3) << 6, 0]
        adc = self.spi.xfer2(buf)
        adcValue = ((adc[1] & 0xF) << 8) | adc[2]
        return adcValue

    def map(self, x, input_min, input_max, output_min, output_max):
        return (x - input_min) * (output_max - output_min) / (input_max - input_min) + output_min

    def set_motor_data(self, motor, state, duty_cycle):
        if motor == 1:  # Control motor 1 (with relay)
            if state == "exhale":
                self.Motor_A_1_PWM.ChangeDutyCycle(0)
                GPIO.output(self.Relay_valve[1], True)
                GPIO.output(self.Relay_valve[0], False)
                self.Motor_A_1_PWM.ChangeDutyCycle(self.duty_cycle)
            elif state == "stop":
                self.Motor_A_1_PWM.ChangeDutyCycle(0)
                GPIO.output(self.Relay_valve[0], False)
                GPIO.output(self.Relay_valve[1], False)
        elif motor == 2:  # Control motor 2 (without relay)
            if state == "inhale":
                self.Motor_B_1_PWM.ChangeDutyCycle(0)
                self.Motor_B_1_PWM.ChangeDutyCycle(self.duty_cycle)
            elif state == "stop":
                self.Motor_B_1_PWM.ChangeDutyCycle(0)

    def sensor_monitor(self):
        while self.running:
            sensorInput = self.analogRead(0)
            # self.sensor_value_label.config(text="Sensor 1 Value: {}".format(sensorInput))

            if sensorInput < 500:
                self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1
                self.set_motor_data(2, "inhale", self.duty_cycle)  # Motor 2 keeps inhaling
            time.sleep(0.1)
            if self.stop_all:
                break

    def adjust_duty_cycle(self, increment):
        self.duty_cycle += increment
        if self.duty_cycle < 10:
            self.duty_cycle = 10
        elif self.duty_cycle > 100:
            self.duty_cycle = 100
        print("Duty Cycle set to: {}%".format(self.duty_cycle))

    def grab(self):
        self.running = True
        self.stop_all = False
        self.set_motor_data(1, "exhale", self.duty_cycle)
        self.set_motor_data(2, "inhale", self.duty_cycle)
        self.sensor_thread = Thread(target=self.sensor_monitor)
        self.sensor_thread.start()


    def release(self):
        self.stop_all = True
        self.running = False
        self.set_motor_data(1, "stop", 0)
        self.set_motor_data(2, "stop", 0)

    def emergency_stop(self):
        self.stop_all = True
        self.running = False
        self.set_motor_data(1, "stop", 0)
        self.set_motor_data(2, "stop", 0)
