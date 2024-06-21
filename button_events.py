import spidev
import RPi.GPIO as GPIO
import time
import tkinter as tk
from threading import Thread


class ButtonEventGroup:
    def __init__(self,sensor1_log,sensor2_log) -> None:
        # Initialize self.SPI
        self.sensor1_log  = sensor1_log
        self.sensor2_log  = sensor2_log
        
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
        self.sensor2_threshold_difference = 500
        self.grip_value = None
    def update_sensor_logs(self, sensor1_value, sensor2_value):
        # sensor1_log 업데이트
        self.sensor1_log.config(state=tk.NORMAL)
        self.sensor1_log.insert(tk.END, f"Sensor 1 Value: {sensor1_value}\n")
        self.sensor1_log.config(state=tk.DISABLED)

        # sensor2_log 업데이트
        self.sensor2_log.config(state=tk.NORMAL)
        self.sensor2_log.insert(tk.END, f"Sensor 2 Value: {sensor2_value}\n")
        self.sensor2_log.config(state=tk.DISABLED)

    def analogRead(self, channel):
        buf = [(1 << 2) | (1 << 1) | (channel & 4) >> 2, (channel & 3) << 6, 0]
        adc = self.spi.xfer2(buf)
        adcValue = ((adc[1] & 0xF) << 8) | adc[2]
        return adcValue

    def map(self, x, input_min, input_max, output_min, output_max):
        return (x - input_min) * (output_max - output_min) / (
            input_max - input_min
        ) + output_min
        
        
    def set_motor_data(self, motor, state, duty_cycle):
        if motor == 1:  # Control motor 1 (with relay)
            if state == "exhale":  # Exhale state
                self.Motor_A_1_PWM.ChangeDutyCycle(0)
                GPIO.output(self.Relay_valve[1], True)
                GPIO.output(self.Relay_valve[0], False)
                self.Motor_A_1_PWM.ChangeDutyCycle(duty_cycle)
            elif state == "inhale":  # Inhale state
                self.Motor_A_1_PWM.ChangeDutyCycle(0)
                GPIO.output(self.Relay_valve[0], True)
                GPIO.output(self.Relay_valve[1], False)
                self.Motor_A_1_PWM.ChangeDutyCycle(duty_cycle)
            elif state == "stop":  # Stop state
                self.Motor_A_1_PWM.ChangeDutyCycle(0)
                GPIO.output(self.Relay_valve[0], False)
                GPIO.output(self.Relay_valve[1], False)
        elif motor == 2:  # Control motor 2 (without relay)
            if state == "inhale":  # Inhale state
                self.Motor_B_1_PWM.ChangeDutyCycle(0)
                self.Motor_B_1_PWM.ChangeDutyCycle(duty_cycle)
            elif state == "stop":  # Stop state
                self.Motor_B_1_PWM.ChangeDutyCycle(0)
                
    # def sensor_monitor(self):
    #     # global running, stop_all, duty_cycle, grip_value, sensor2_threshold_difference
    #     while self.running:
    #         sensorInput = self.analogRead(0)
    #         sensorInput2 = self.analogRead(1)
            
    #         self.update_sensor_logs(sensorInput, sensorInput2)
            
    #         if sensorInput > 3000:
    #             self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1
    #         if self.grip_value is not None and (
    #             sensorInput2 >= self.grip_value + self.sensor2_threshold_difference
    #         ):
    #             self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1

    #         self.set_motor_data(
    #             2, "inhale", self.duty_cycle
    #         )  # Motor 2 continues to inhale

    #         time.sleep(0.1)
    #         if self.stop_all:
    #             break
    # def sensor_monitor(self):
    #     # global running, stop_all, duty_cycle, grip_value, sensor2_threshold_difference
        
    #     start_time = time.time()
    #     during_time = 0
        
    #     while self.running:
    #         current_time = time.time()
    #         sensorInput = self.analogRead(0)
    #         sensorInput2 = self.analogRead(1)
            
    #         self.update_sensor_logs(sensorInput, sensorInput2)
    #         during_time = start_time - current_time
    #         if sensorInput > 3000 or during_time>4:
    #             self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1
            
    #         elif self.grip_value is not None and (
    #             sensorInput2 >= self.grip_value + self.sensor2_threshold_difference
    #         ):
    #             self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1

    #         self.set_motor_data(
    #             2, "inhale", self.duty_cycle
    #         )  # Motor 2 continues to inhale

    #         time.sleep(0.1)
    #         if self.stop_all:
    #             break
    def sensor_monitor(self):
        # global running, stop_all, duty_cycle, grip_value, sensor2_threshold_difference
        
        start_time = time.time()
        during_time = 0
        
        while self.running:
            current_time = time.time()
            sensorInput = self.analogRead(0)
            sensorInput2 = self.analogRead(1)
            
            self.update_sensor_logs(sensorInput, sensorInput2)
            
            during_time = start_time - current_time
            
            
            if during_time> 4:
                self.set_motor_data(1, "stop", self.duty_cycle)
            elif sensorInput > 3000:
                self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1
            
            elif self.grip_value is not None and (sensorInput2 >= self.grip_value + self.sensor2_threshold_difference):
                self.set_motor_data(1, "stop", self.duty_cycle)  # Stop motor 1

            self.set_motor_data(
                2, "inhale", self.duty_cycle
            )  # Motor 2 continues to inhale

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
        self.grip_value = self.analogRead(1)
        self.running = True
        self.stop_all = False
        self.set_motor_data(1, "exhale", self.duty_cycle)
        self.set_motor_data(2, "inhale", self.duty_cycle)
        self.sensor_thread = Thread(target=self.sensor_monitor)
        self.sensor_thread.start()

    # def release(self):
    #     self.stop_all = True
    #     self.running = False
    #     self.set_motor_data(2, "stop", 0)  # Stop motor 2 immediately
    #     self.set_motor_data(1, "inhale", self.duty_cycle)  # Start motor 1 inhale
    #     while abs(self.analogRead(1) - self.grip_value) > 100:
    #         time.sleep(0.1)
    #     self.set_motor_data(1, "stop", 0)  # Stop motor 1 when sensor 2 value is close to the initial value
    def release(self):
        self.stop_all = True
        self.running = False
        self.set_motor_data(2, "stop", 0)  # Stop motor 2 immediately
        self.set_motor_data(1, "inhale", self.duty_cycle)  # Start motor 1 inhale
        start_time = time.time()
        while (1):
            current_time = time.time()
            during_time = current_time - start_time
            if during_time > 4:
                break
        self.set_motor_data(1, "stop", 0)  # Stop motor 1 when sensor 2 value is close to the initial value
    def emergency_stop(self):
        self.stop_all = True
        self.running = False
        self.set_motor_data(1, "stop", 0)
        self.set_motor_data(2, "stop", 0)
