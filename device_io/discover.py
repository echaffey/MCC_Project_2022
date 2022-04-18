from mcculw import ul
from mcculw.enums import InterfaceType
from mcculw.device_info import DaqDeviceInfo

# from mcculw.ul import ULError
from mcculw.enums import InfoType, BoardInfo, ULRange

from settings import Settings


class DiscoverDevice:
    """
    Object used to discover, connect, disconnect and assign board numbers to connected DAQ devices.

        Methods:
            search_for_devices() :  Identifies connected DAQ device names.
            create_device_num()  :  Assigns a board number to a device.
            disconnect_device()  :  Unassigns the board number from a connected device.
    """

    def __init__(self):

        # Initialize the selected board number and list of connected devices
        self._devices = None
        self._list_board_nums = []

        # Ignore anything currently connected to DAQ via InstaCal to prevent issues
        ul.ignore_instacal()

    def search_for_devices(self) -> tuple:
        """Find all connected devices and assign a board number to each of them."""

        # Use the Universal Library to find all connected devices
        self._devices = ul.get_daq_device_inventory(InterfaceType.ANY)

        [print(str(device)) for device in self._devices if len(self._devices) > 0]

        self._create_device_num()

        channel_1 = Settings.DAC_OUTPUT_CHANNEL_1
        channel_2 = Settings.DAC_OUTPUT_CHANNEL_2
        dac_board = Settings.DAC_BOARD_NUM

        # IMPORTANT:  Manually set the voltage range for the USB-3101 to -10 to 10V
        # If removed, the device defaults to 0 to 10V and the motors can only move
        # in a single direction.
        # The documentation for this function is incorrect. Parameters should be:
        # set_config(info_type: InfoType, board_num: int, channel_num: int, config_parameter: BoardInfo, config_value: Any)
        ul.set_config(
            InfoType.BOARDINFO,
            dac_board,
            channel_1,
            BoardInfo.DACRANGE,
            ULRange.BIP10VOLTS,
        )
        ul.set_config(
            InfoType.BOARDINFO,
            dac_board,
            channel_2,
            BoardInfo.DACRANGE,
            ULRange.BIP10VOLTS,
        )

        return self.get_devices()

    def _create_device_num(self, announce: bool = False) -> None:
        """Assigns a board number to each of the DAQ devices found."""

        if len(self._devices) > 0:
            for i, device in enumerate(self._devices):

                # Retrieve the unique ID number of the device
                device_id = device.unique_id

                # Assign the device a board number
                ul.create_daq_device(i, device)

                # Add to the list of board numbers
                self._list_board_nums.append(i)

                # Broadcast connection to terminal
                if announce:
                    print(f"Created {device} (ID: {device_id}) on Board {i}")

    def disconnect_devices(self, board: int = None) -> None:
        """
        Disconnect from one or all DAQ devices.

            Parameters:
                board(int):  Optional. Individual board number to disconnect.
        """
        if board is not None:
            ul.release_daq_device(board)
            # self._list_board_nums[board].remove()
        else:
            # Iterate through the currently connected devices and disconnect
            if len(self._list_board_nums) > 0:
                [ul.release_daq_device(num) for num in self._list_board_nums]
                self._list_board_nums = []

    def reassign_board_num(self, curr_board: int, new_board_num: int) -> None:
        """
        Reassigns the board number of a currently connected DAQ device.

            Parameters:
                curr_board(int): Board number of the currently connected device.
                new_board_num(int):  New board number to be assigned.
        """
        if DaqDeviceInfo(curr_board) is not None:
            self.disconnect_devices(curr_board)
            ul.create_daq_device(new_board_num, self._devices[curr_board])
            self._list_board_nums[curr_board] = new_board_num

    def get_devices(self) -> tuple:
        """
        Returns a tuple containing the connected devices and their associated board numbers.

            Returns:
                DAQ_board(DaqDeviceDescriptor) : DAQ Board object.
                device_ID(str): Unique device identification number.
                board_number(int): Assigned board number.
        """

        # Tuple containing the device name and its assigned board number
        return tuple(zip(self._devices, self._list_board_nums))


if __name__ == "__main__":
    disc = DiscoverDevice()

    disc.search_for_devices()

    board_0 = DaqDeviceInfo(0)
    # print(ul.a_in(0, 0, board_0.get_ai_info()))

    disc.disconnect_devices()
