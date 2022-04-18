from mcculw import ul
from mcculw.enums import DigitalIODirection
from mcculw.device_info import DaqDeviceInfo


def set_digital_out(board_num: int = 0, bit_value: int = 0) -> None:

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

    # Get the supported range of values
    dio_info = device.get_dio_info()

    # Find the first port that supports input, defaults to None if nothing is found.
    port = next((port for port in dio_info.port_info if port.supports_input), None)

    if not port:
        raise Exception(
            f"The device connected to board {board_num} does not support digital input"
        )

    # Configure the port for input if able.
    if port.is_port_configurable:
        ul.d_config_port(board_num, port.type, DigitalIODirection.OUT)

    # Set the port value to 255 (8 bit value)
    port_value = 0xFF

    # Output the value to the port
    ul.d_out(board_num, port.type, port_value)

    bit_num = 0
    print("Setting", port.type.name, "bit", bit_num, "to", bit_value)

    # Output the value to the bit
    ul.d_bit_out(board_num, port.type, bit_num, bit_value)
