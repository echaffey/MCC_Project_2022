from mcculw import ul
from mcculw.enums import DigitalIODirection
from mcculw.device_info import DaqDeviceInfo


def get_digital_input(board_num: int = 0, bit_number: int = 0):
    """
    Reads the digital input on a given bit from an A2D board.

    Parameters:
        board_num (int) : Instacal or DAQ board number associated with the device.
        bit_number (int) : Bit number to read from. Values are in the range from 0 to 7
    """
    try:
        device = DaqDeviceInfo(board_num)
    except Exception as e:
        print(
            f"Error in trying to connect to the device on board number {board_num}/n/n"
            "Error: /n{e}"
        )
    finally:
        pass

    # Check to make sure that analog connection is supported
    if not device.supports_digital_io:
        raise Exception("Error: The DAQ device does not support digital input/output")

    # Get the supported range of values and set the channel to use
    dio_info = device.get_dio_info()

    # Find the first port that supports input, defaults to None if nothing is found.
    port = next((port for port in dio_info.port_info if port.supports_input), None)

    if not port:
        raise Exception(
            f"The device connected to board {board_num} does not support digital input"
        )

    # Configure the port for input if able.
    if port.is_port_configurable:
        ul.d_config_port(board_num, port.type, DigitalIODirection.IN)

    # Read in a value from the digital port
    port_value = ul.d_in(board_num, port.type)

    # Get a value from the first digital bit
    bit_num = bit_number
    bit_value = ul.d_bit_in(board_num, port.type, bit_num)

    return bit_value, port_value
