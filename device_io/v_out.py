from mcculw import ul
from mcculw.device_info import DaqDeviceInfo
from mcculw.enums import (
    DigitalIODirection,
    DigitalPortType,
    ULRange,
    InfoType,
    BoardInfo,
)


def set_output_voltage(board_num: int, channel: int, voltage: float = 0) -> None:

    # Get the device info
    device = DaqDeviceInfo(board_num)

    # Check that the device can support outputting an analog voltage
    if not device.supports_analog_output:
        raise Exception("Error: The DAQ device does not support analog output")

    ao_info = device.get_ao_info()
    print(ao_info.num_chans)
    # Check the supported voltage output range of the device
    ao_range = ao_info.supported_ranges[0]
    # print(ao_range)
    ao_range = ULRange.BIP10VOLTS
    ul.a_out(board_num, channel, ao_range, voltage)
    # ul.v_out(board_num, channel, ao_range, voltage)


def volt_out(board_num: int, channel: int, voltage: float):
    # https://github.com/LauLauThom/USB-3101--MeasurementComputing/blob/master/USB-3101.py

    # Page 41 - https://github.com/LauLauThom/USB-3101--MeasurementComputing/blob/master/UniversalLibrariesFunctionReference.pdf
    # Page 65 - https://pim-resources.coleparmer.com/data-sheet/sm-ul-functions.pdf

    # Get the device info
    device = DaqDeviceInfo(board_num)

    # Check that the device can support outputting an analog voltage
    if not device.supports_analog_output:
        raise Exception("Error: The DAQ device does not support analog output")

    # Get the boards assigned voltage output range
    ao_range = ul.get_config(InfoType.BOARDINFO, 1, channel, BoardInfo.DACRANGE)

    # Convert voltage values to 16-bit integer data values
    v_out = ul.from_eng_units(1, ao_range, voltage)

    # Send voltage to the board
    ul.a_out(board_num, channel, ao_range, v_out)


def set_bit_on(bit_channel: int):
    ul.d_config_bit(1, DigitalPortType.AUXPORT, bit_channel, DigitalIODirection.OUT)
    ul.d_bit_out(1, DigitalPortType.AUXPORT, bit_channel, 1)
