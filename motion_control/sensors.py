from typing import Union

from mcculw import ul

from device_io.analog_in import get_analog_input
from device_io.wrapper_new import cb_C7266_config


class MotorEncoder:
    """
    Defines a Measurement Computing C7266 Quad-04 Encoder board.
    """

    def __init__(self, board_num: int):
        # Initialize encoder board
        self.board_num = board_num

        self.configure_parameters()

    def configure_parameters(self):
        """
        Initializes each of the 4 channels on the encoder board.  The function
        cb_C7266_config is a custom written C wrapper which is not included in the
        MCC Universal Library code due to the board no longer being supported.
        """
        # Initialize encoder board
        cb_C7266_config(0, 1, 4, 0, 2, 0, 0, 1, 0)
        cb_C7266_config(0, 2, 4, 0, 2, 0, 0, 1, 0)
        cb_C7266_config(0, 3, 0, 0, 2, 0, 0, 1, 0)
        cb_C7266_config(0, 4, 0, 0, 2, 0, 0, 1, 0)

    def get_counter_value(self, counter_num: int) -> int:
        """
        Reads in the value on the specified counter.

        Args:
            counter_num (int): Counter number to read.  This value ranges from 1 to 4.

        Returns:
            int: Encoder counter value.
        """
        val = ul.c_in(self.board_num, counter_num)

        return val

    def get_all_counter_values(self) -> list:
        """
        Returns a list containing the encoder counter values on all channels.

        Returns:
            list: Encoder values on channels 1 through 4.
        """
        vals = [ul.c_in(self.board_num, c) for c in [1, 2, 3, 4]]

        return vals

    def zero_counter(self, counter_num: int):
        """UNIMPLEMENTED. NOT SUPPORTED BY THIS BOARD"""
        ul.c_clear(self.board_num, counter_num)


class LaserSensor:
    """
    Defines a laser measurement sensor device.
    """

    def __init__(self, board_num: int, channel_num: int):
        self.board_num = board_num
        self.channel_num = channel_num

    def read_laser_value(self) -> Union[int, int]:
        """Returns the value and engineering value from the laser"""
        return get_analog_input(self.board_num, self.channel_num)