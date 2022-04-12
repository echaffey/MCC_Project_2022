from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError, win_buf_alloc, win_buf_free
from mcculw.device_info import DaqDeviceInfo

# from discover import DiscoverDevice


def get_analog_input(board_num: int, channel: int):

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

    # value = ul.a_in_scan(board_num, 0, 10, 1,10,ai_range, win_buf_alloc(8), 32)

    return value, eng_units_value
