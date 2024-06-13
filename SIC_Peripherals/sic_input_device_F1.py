import random

from SIC_Utilities.sic_constants import SW_EQUAL, SW_LESS_THAN
from SIC_Utilities.sic_converter import dec_to_hex_string
from SIC_Utilities.sic_messaging import print_error


def read_byte_input_device_F1(is_in_EOF_state: bool):
    TEXT_COLOR_CYAN = "\033[96m"
    TEXT_COLOR_DEFAULT = "\033[0m"
    WAITING_ON_VALID_INPUT = True

    while WAITING_ON_VALID_INPUT:
        print(TEXT_COLOR_CYAN + "Enter one character ('\\n' for newline)" + TEXT_COLOR_DEFAULT)

        if is_in_EOF_state:
            print(TEXT_COLOR_CYAN + "or enter 'EOF' to indicate End of File" + TEXT_COLOR_DEFAULT)
            input_string = input(TEXT_COLOR_CYAN + "INPUT DEVICE> " + TEXT_COLOR_DEFAULT)
            print("")  # Put space before next register dump
            if input_string == "EOF":
                return "00"
        else:
            print(TEXT_COLOR_CYAN + "or enter 'EOR' to indicate End of Record" + TEXT_COLOR_DEFAULT)
            input_string = input(TEXT_COLOR_CYAN + "INPUT DEVICE> " + TEXT_COLOR_DEFAULT)
            print("")  # Put space before next register dump
            if input_string == "EOR":
                return "00"

        if input_string == "\\n":
            # Return ascii code for LF (line feed)
            return "0A"
        elif len(input_string) == 1:
            dec_ascii_value = ord(input_string)
            return dec_to_hex_string(dec_ascii_value)
        else:
            print_error("INPUT PERIPHERAL DEVICE FAULT")


def test_input_device_F1():
    # Simulate testing a device by randomly selecting
    # READY (SW_LESS_THAN) or NOT READY (SW_EQUAL).
    # Randomization weighted to favor NOT READY
    test_device_response_list = [SW_EQUAL, SW_EQUAL, SW_LESS_THAN]
    test_device_response_hex_string = random.choice(test_device_response_list)

    return test_device_response_hex_string


