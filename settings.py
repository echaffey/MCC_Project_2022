from dataclasses import dataclass


@dataclass
class Settings:
    """
    H-Frame positioner global application configuration
    """

    """
    Device Settings
    ---------------------------------------------------------------------------------------------
    """
    # Get these board numbers from InstaCal
    ENCODER_BOARD_NUM: int = 0  # PCI-QUAD04 board
    DAC_BOARD_NUM: int = 1  # USB_3101 board
    ADC_BOARD_NUM: int = 2  # USB-1408FS board

    MOTOR_VOLTAGE_MAX: int = 10  # Maximum allowable bipolar voltage allowed
    MOTOR_VOLTAGE_OUT: float = 3.0  # Default motor voltage output value

    ENCODER_RESOLUTION: int = 0

    MOTOR_1_CHANNEL: int = 0
    MOTOR_2_CHANNEL: int = 1

    LASER_1_CHANNEL: int = 0
    LASER_2_CHANNEL: int = 1

    """
    GUI Settings
    ----------------------------------------------------------------------------------------------
    """
    WIDTH: int = 600  # window size when starting up the application
    HEIGHT: int = 600

    MAX_WIDTH: int = 800
    MAX_HEIGHT: int = 800

    CANVAS_SIZE: int = 400

    HZ: int = 60  # Frequency to read from the devices
    TIME_DELTA = 1 / HZ

    BG_COLOR: str = "#444444"
    BTN_COLOR: str = "#666666"

    """General Settings"""
    APP_NAME: str = "H-Frame Positioner GUI"
    VERSION: str = "0.0.1"
    SPONSOR: str = "Musa Jouaneh"
    AUTHOR: str = "Evan Chaffey"
    ORGANIZATION: str = "University of Rhode Island"
    YEAR: str = "2022"

    GITHUB_URL: str = ""
    GITHUB_URL_README: str = ""

    USER_SETTINGS_PATH: str = ""

    ABOUT_TEXT: str = (
        f"{APP_NAME} Version {VERSION} © {YEAR} {SPONSOR}, {AUTHOR}, {ORGANIZATION}"
    )
