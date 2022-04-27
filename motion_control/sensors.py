from typing import Union

from mcculw import ul

# Import libraries included with this project
from device_io.analog_in import get_analog_input
from device_io.wrapper_new import cb_C7266_config
from device_io.digital_in import get_digital_input


class MotorEncoder:
    """
    Defines a Measurement Computing C7266 Quad-04 Encoder board.
    """

    def __init__(self, board_num: int):
        # Initialize encoder board
        self.board_num = board_num

        self._configure_board()

    def _configure_board(self):
        """
        Initializes each of the 4 channels on the encoder board.  The function
        cb_C7266_config is a custom implementation C wrapper which is not included in the
        MCC Universal Library code due to the board no longer being supported.
        """

        # Configure the 4 channels of the QUAD04 Encoder
        # Encoders are set to unsigned short and output values 0 to 65536
        # Quadrature value of 4 is highest resolution
        cb_C7266_config(0, 1, 4, 0, 2, 0, 0, 1, 0)
        cb_C7266_config(0, 2, 4, 0, 2, 0, 0, 1, 0)
        cb_C7266_config(0, 3, 4, 0, 2, 0, 0, 1, 0)
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

    def zero_counter(self, counter_num: int) -> None:
        """UNIMPLEMENTED. NOT SUPPORTED BY THIS BOARD"""
        ul.c_clear(self.board_num, counter_num)


class LaserSensor:
    """
    Defines a laser measurement sensor.
    """

    def __init__(self, board_num: int, channel_num: int):

        # Stores the board and channel number for the device
        self.board_num = board_num
        self.channel_num = channel_num

    def read_laser_value(self) -> Union[int, int]:
        """Returns the value and engineering value (voltage) from the laser"""
        return get_analog_input(self.board_num, self.channel_num)


class LimitSensors:
    """
    Defines a collection of limit switch sensors.
    """

    def __init__(self, board_num: int, channel_nums: list, port_num: int = 0):
        self.board_num = board_num
        self.channels = channel_nums
        self.port_num = port_num

    def is_activated(self, channel_num: int) -> bool:
        """
        Checks to see if a selected limit switch has been triggered.

        Args:
            channel_num (int): Bit number of the limit switch.

        Returns:
            bool: True if the switch has been triggered.
        """
        if (
            get_digital_input(
                board_num=self.board_num,
                bit_number=channel_num,
                port=self.port_num,
            )
            > 0
        ):
            return True

        return False

    def read_switches(self) -> list:
        """
        Reads state values from all of the limit switches.

        Returns:
            list: List of limit switch state values.
        """
        return [
            get_digital_input(
                board_num=self.board_num, bit_number=channel, port=self.port_num
            )[0]
            for channel in self.channels
        ]
