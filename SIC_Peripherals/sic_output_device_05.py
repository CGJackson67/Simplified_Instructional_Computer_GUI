import random

from SIC_Utilities.sic_constants import SW_EQUAL, SW_LESS_THAN
from SIC_Utilities.sic_converter import hex_string_to_dec

OUTPUT_DEVICE_05_INTERFACE = ""


def initialize_output_device_05():
    global OUTPUT_DEVICE_05_INTERFACE

    OUTPUT_DEVICE_05_INTERFACE = ""


def test_output_device_05():
    # Simulate testing a device by randomly selecting
    # READY (SW_LESS_THAN) or NOT READY (SW_EQUAL).
    # Randomization weighted to favor NOT READY
    test_device_response_list = [SW_EQUAL, SW_EQUAL, SW_LESS_THAN]
    test_device_response_hex_string = random.choice(test_device_response_list)

    return test_device_response_hex_string


def write_byte_to_output_device_05(byte_string: str):
    global OUTPUT_DEVICE_05_INTERFACE
    TEXT_COLOR_CYAN = "\033[96m"
    TEXT_COLOR_DEFAULT = "\033[0m"

    dec_ascii_value = hex_string_to_dec(byte_string)
    OUTPUT_DEVICE_05_INTERFACE += chr(dec_ascii_value)

    print(TEXT_COLOR_CYAN + "OUTPUT DEVICE>\n" + OUTPUT_DEVICE_05_INTERFACE + "\n" + TEXT_COLOR_DEFAULT)

