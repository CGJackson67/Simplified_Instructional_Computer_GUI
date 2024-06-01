from SIC_Utilities.sic_constants import DEC_TO_HEX_DICT, MINIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_MEMORY_ADDRESS_DEC, \
    MEMORY_ADDRESS_STRING_LENGTH, HEX_TO_DEC_DICT, HEX_DIGIT_SET, BIN_TO_HEX_DICT, HEX_TO_BIN_DICT, BITS_IN_WORD


class SICConverterError(Exception):
    pass


def dec_to_hex_string(dec_value: int):
    if not isinstance(dec_value, int):
        raise SICConverterError("Cannot convert non-integer value passed to dec_to_hex_string function")

    hex_digit_list = []

    quotient = dec_value
    while quotient != 0:
        remainder = quotient % 16

        if remainder < 10:
            hex_digit_list.insert(0, str(remainder))
        else:
            hex_digit_list.insert(0, DEC_TO_HEX_DICT[remainder])

        quotient = quotient // 16

    hex_string = ""

    for hex_digit in hex_digit_list:
        hex_string += hex_digit

    return hex_string


# NOTE: Do we want to check for out of range and other errors?
#       Do we want read and write memory functions?
def dec_to_memory_address_hex_string(dec_value: int):
    if not isinstance(dec_value, int):
        raise SICConverterError("Cannot convert non-integer value passed to dec_to_memory_address_hex_string function")

    if dec_value < MINIMUM_MEMORY_ADDRESS_DEC or dec_value > MAXIMUM_MEMORY_ADDRESS_DEC:
        raise SICConverterError("Memory address must be in the range 0 to 32767")

    hex_digit_list = list(dec_to_hex_string(dec_value))

    # Pad hex_string_list with leading zeros until
    # its length is MEMORY_ADDRESS_STRING_LENGTH
    while len(hex_digit_list) < MEMORY_ADDRESS_STRING_LENGTH:
        hex_digit_list.insert(0, "0")

    hex_string = ""

    for hex_digit in hex_digit_list:
        hex_string += hex_digit

    return hex_string


def hex_string_to_dec(hex_string: str):
    if not isinstance(hex_string, str):
        raise SICConverterError("Cannot convert non-string value passed to hex_string_to_dec function")

    hex_digit_list = list(hex_string)
    reversed_hex_digit_list = list(reversed(hex_digit_list))

    dec_value = 0

    for index in range(len(reversed_hex_digit_list)):
        hex_digit = reversed_hex_digit_list[index]

        if hex_digit not in HEX_TO_DEC_DICT:
            raise SICConverterError("Invalid hex digit (0-9,A-F)")

        dec_value += HEX_TO_DEC_DICT[hex_digit] * 16 ** index

    return dec_value


def test_for_hex(hex_string):
    for char in hex_string:
        if char not in HEX_DIGIT_SET:
            return False

    return True


def bin_word_to_hex_word(bin_word_string):
    hex_word_string = ""
    # Register holds 24 bits
    bin_word_string = bin_word_string.rjust(BITS_IN_WORD, "0")
    # range(START, STOP, STEP)
    for index in range(0, BITS_IN_WORD, 4):
        hex_word_string += BIN_TO_HEX_DICT[bin_word_string[index:index + 4]]

    return hex_word_string


def hex_word_to_bin_word(hex_word_string):
    bin_word_string = ""
    # Register holds 24 bits
    hex_word_string = hex_word_string.rjust(6, "0")

    for hex_digit in hex_word_string:
        bin_word_string += HEX_TO_BIN_DICT[hex_digit]

    return bin_word_string
