from dataclasses import dataclass


@dataclass
class Settings:
    """
    H-Frame positioner global application configuration.

    Change the variable values in this file to modify how the program runs, which
    board numbers the devices are on and which channels each sensor is on.
    """

    """
    Device Settings
    ---------------------------------------------------------------------------------------------
    """
    # Get these board numbers from InstaCal
    ENCODER_BOARD_NUM: int = 0  # PCI-QUAD04 board
    DAC_BOARD_NUM: int = 1  # USB_3101 board
    ADC_BOARD_NUM: int = 2  # USB-1408FS board

    MOTOR_VOLTAGE_MAX: int = 10  # Maximum possible bipolar voltage allowed
    MOTOR_VOLTAGE_ALLOWABLE: float = 5.0  # Maximum allowable voltage to the motor
    MOTOR_VOLTAGE_DEFAULT: float = 3.0  # Default motor voltage output value

    # These are the channels on the physical board
    MOTOR_1_CHANNEL: int = 0
    MOTOR_2_CHANNEL: int = 1

    # Analog channels to which the lasers are connected on the USB-1408FS board
    LASER_1_CHANNEL: int = 0
    LASER_2_CHANNEL: int = 1

    # Digital channels to which the limit switches are connected on the USB-1408FS board
    LIMIT_PORT: int = 0  # Port A, Port B = 1
    LIMIT_S1: int = 0  # Limit Sensor 1, Channel 0
    LIMIT_S2: int = 1  # Limit Sensor 2, Channel 1
    LIMIT_S3: int = 2  # Limit Sensor 3, Channel 2
    LIMIT_S4: int = 3  # Limit Sensor 4, Channel 3
    LIMIT_S5: int = 4  # Limit Sensor 5, Channel 4
    LIMIT_S6: int = 5  # Limit Sensor 6, Channel 5
    LIMIT_SENSORS = [LIMIT_S1, LIMIT_S2, LIMIT_S3, LIMIT_S4, LIMIT_S5, LIMIT_S6]

    """
    Kinematics
    ---------------------------------------------------------------------------------------------
    """

    MOTOR_GEAR_RATIO: float = 5.9  # 5.9:1 gear reduction ratio

    PULLEY_RADIUS: float = 0.75  # inches

    ENCODER_VALUES: int = 2**16 - 1  # 16-bit values
    ENCODER_RESOLUTION: int = 512  # Lines per one revolution of the motor shaft
    QUADRATURE: int = 4
    ENCODER_VALS_PER_REV: int = (
        ENCODER_RESOLUTION * QUADRATURE * MOTOR_GEAR_RATIO
    )  # Number of encoder values per revolution

    """
    GUI Settings
    ----------------------------------------------------------------------------------------------
    """
    WIDTH: int = 600  # window size when starting up the application
    HEIGHT: int = 600

    MAX_WIDTH: int = 800  # Maximum allowable window size
    MAX_HEIGHT: int = 800

    CANVAS_SIZE: int = 400

    HZ: int = 60  # Frequency to read from the devices
    TIME_DELTA = 1 / HZ

    BG_COLOR: str = "#444444"  # Window background color
    BTN_COLOR: str = "#666666"  # Button color

    """General Settings"""
    APP_NAME: str = "H-Frame Positioner GUI"
    VERSION: str = "0.0.1"
    PROFESSOR: str = "Musa Jouaneh"
    AUTHOR: str = "Evan Chaffey"
    ORGANIZATION: str = "University of Rhode Island"
    YEAR: str = "2022"

    GITHUB_URL: str = ""
    GITHUB_URL_README: str = ""

    USER_SETTINGS_PATH: str = ""

    ABOUT_TEXT: str = (
        f"{APP_NAME} Version {VERSION} © {YEAR} {PROFESSOR}, {AUTHOR}, {ORGANIZATION}"
    )
