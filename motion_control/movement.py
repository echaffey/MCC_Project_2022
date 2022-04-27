from dataclasses import dataclass
from device_io.v_out import volt_out
from settings import Settings
import time

import numpy as np

motor_board_num = Settings.DAC_BOARD_NUM
motor_1 = Settings.MOTOR_1_CHANNEL
motor_2 = Settings.MOTOR_2_CHANNEL


@dataclass
class Speed:
    speed_1 = 0.5
    speed_2 = 0.5


def stop_motors():
    """
    Stops all voltage output to the motors.
    """
    Speed.speed_1 = 0
    Speed.speed_2 = 0
    volt_out(motor_board_num, motor_1, 0)
    volt_out(motor_board_num, motor_2, 0)


def pos_X(voltage: float):
    """Moves the end effector in the defined positive x direction."""
    stop_motors()
    Speed.speed_1 = -voltage
    Speed.speed_2 = voltage
    volt_out(motor_board_num, motor_1, -voltage)
    volt_out(motor_board_num, motor_2, voltage)


def neg_X(voltage: float):
    """Moves the end effector in the defined negative x direction."""
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = -voltage
    # print(speed_1, speed_2)
    volt_out(motor_board_num, motor_1, voltage)
    volt_out(motor_board_num, motor_2, -voltage)


def pos_Y(voltage: float):
    """Moves the end effector in the defined positive y direction."""
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = voltage
    volt_out(motor_board_num, motor_1, voltage)
    volt_out(motor_board_num, motor_2, voltage)


def neg_Y(voltage: float):
    """Moves the end effector in the defined negative x direction."""
    stop_motors()
    Speed.speed_1 = -voltage
    Speed.speed_2 = -voltage
    volt_out(motor_board_num, motor_1, -voltage)
    volt_out(motor_board_num, motor_2, -voltage)


def ne(voltage: float):
    """
    Moves the end effector in the northeast direction (+X, -Y)

    Args:
        voltage (float): Voltage to apply, in engineering units.
    """
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = 0

    volt_out(motor_board_num, motor_2, Speed.speed_1)


def se(voltage: float):
    """
    Moves the end effector in the southeast direction (-X, -Y)

    Args:
        voltage (float): Voltage to apply, in engineering units.
    """
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = 0

    volt_out(motor_board_num, motor_1, Speed.speed_1)


def nw(voltage: float):
    """
    Moves the end effector in the northwest direction (+X, +Y)

    Args:
        voltage (float): Voltage to apply, in engineering units.
    """
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = 0

    volt_out(motor_board_num, motor_1, -Speed.speed_1)


def sw(voltage: float):
    """
    Moves the end effector in the southwest direction (-X, -Y)

    Args:
        voltage (float): Voltage to apply, in engineering units.
    """
    stop_motors()
    Speed.speed_1 = voltage
    Speed.speed_2 = 0

    volt_out(motor_board_num, motor_2, -Speed.speed_1)
    # volt_out(motor_board_num, motor_2, -Speed.speed_2)


def slow_pos_y(sensor_input: float, volts: float):
    v_out = abs(sensor_input / 10) * volts
    print(v_out)
    volt_out(motor_board_num, motor_1, v_out)
    volt_out(motor_board_num, motor_2, v_out)


def adjust_speed(sensor_input: float):
    v_out = abs(sensor_input / 10) * Speed.speed_1

    print(Speed.speed_1, v_out)
    volt_out(motor_board_num, motor_1, v_out)
    volt_out(motor_board_num, motor_2, v_out)


def draw_square(voltage: float):
    """
    Moves the end effector in a square pattern.

    Args:
        voltage (float): Voltage to be applied to the motors, in engineering units.
    """

    time_sleep = 1.5 / voltage
    stop_motors()
    neg_X(voltage)
    time.sleep(time_sleep)
    neg_Y(voltage)
    time.sleep(time_sleep)
    pos_X(voltage)
    time.sleep(time_sleep)
    pos_Y(voltage)
    time.sleep(time_sleep)
    stop_motors()


def draw_diamond(voltage: float):
    """
    Moves the end effector in a diamond pattern.

    Args:
        voltage (float): Voltage to be applied to the motors, in engineering units.
    """
    time_sleep = np.sqrt(2 * 1.5 ** 2) / voltage
    print(np.sqrt(2 * 1.5 ** 2))
    stop_motors()

    sw(voltage)
    time.sleep(time_sleep)

    nw(voltage)
    time.sleep(time_sleep)

    ne(voltage)
    time.sleep(time_sleep)

    se(voltage)
    time.sleep(time_sleep)
    stop_motors()
