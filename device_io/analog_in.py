from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError, win_buf_alloc, win_buf_free
from mcculw.device_info import DaqDeviceInfo


def get_analog_input(board_num: int, channel: int):
    """
    Reads the analog input signal from the device's `board_num` on the board's input `channel`.

    Args:
        board_num (int): Instacal defined board number for the input device.
        channel (int): Input channel to read from.

    Raises:
        Exception: If the board that you're trying to connect to does not exists.

    Returns:
        (value, eng_units): Returns the bit value and its equivalent engineering units.
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
    if not device.supports_analog_input:
        raise Exception("Error: The DAQ device does not support analog input")

    # Get the supported range of values and set the channel to use
    ai_info = device.get_ai_info()

    ai_range = ai_info.supported_ranges[0]
    ai_range = ULRange.BIP10VOLTS
    # channel = 0

    # Get a value from the device
    if ai_info.resolution <= 16:
        # Use the a_in method for devices with a resolution <= 16
        value = ul.a_in(board_num, channel, ai_range)
        # Convert the raw value to engineering units
        eng_units_value = ul.to_eng_units(board_num, ai_range, value)
    else:
        # Use the a_in_32 method for devices with a resolution > 16
        # (optional parameter omitted)
        value = ul.a_in_32(board_num, channel, ai_range)
        # Convert the raw value to engineering units
        eng_units_value = ul.to_eng_units_32(board_num, ai_range, value)

    return value, eng_units_value
