from SIC_Utilities.sic_constants import NUMBER_OF_BITS_IN_AN_INTEGER, MINIMUM_INTEGER, MAXIMUM_INTEGER, HEX_TO_BIN_DICT, \
    BIN_TO_HEX_DICT


class SICIntegerError(Exception):
    pass


def bin_string_to_dec(bin_value_string: str):
    # Check for invalid input
    # Make sure bin_value is a string
    # Make sure bin_value_string is proper length
    # Make sure bin_value_string represents a
    # binary number comprised of 1's and 0's
    if ((not isinstance(bin_value_string, str)) or
            (len(bin_value_string) != NUMBER_OF_BITS_IN_AN_INTEGER) or
            (bin_value_string.count("0") + bin_value_string.count("1") != NUMBER_OF_BITS_IN_AN_INTEGER)):
        raise SICIntegerError("Invalid binary value string")

    # Convert bin_value_string to list
    binary_digit_list = []
    for binary_digit in bin_value_string:
        binary_digit_list.append(int(binary_digit))

    # Determine if bin_value_string is negative
    is_negative = False
    if binary_digit_list[0] == 1:
        is_negative = True
        # Reverse 2's Compliment
        # Step 1: Subtract 1 from bin_value_string
        for index in reversed(range(NUMBER_OF_BITS_IN_AN_INTEGER)):
            match binary_digit_list[index]:
                case 0:
                    binary_digit_list[index] = 1
                case 1:
                    binary_digit_list[index] = 0
                    break

        # Step 2: Flip all the bits
        for index in range(NUMBER_OF_BITS_IN_AN_INTEGER):
            if binary_digit_list[index] == 0:
                binary_digit_list[index] = 1
            else:
                binary_digit_list[index] = 0

    # Convert binary value to decimal value
    reversed_binary_digit_list = list(reversed(binary_digit_list))
    dec_value = 0
    for index in range(NUMBER_OF_BITS_IN_AN_INTEGER):
        dec_value += reversed_binary_digit_list[index] * 2 ** index

    # Convert dec_value to negative
    # if the binary value was negative
    if is_negative:
        dec_value *= -1

    return dec_value


# TEST BED
# try:
#     dec_value = bin_string_to_dec("101010101010101010101010")
#     print("dec_value 1:", dec_value)
#     dec_value = bin_string_to_dec("101010101010101010101111")
#     print("dec_value 2:", dec_value)
#     dec_value = bin_string_to_dec("000000001100000000111110")
#     print("dec_value 3:", dec_value)
#     dec_value = bin_string_to_dec("000000000000000000111001")
#     print("dec_value 4:", dec_value)
#     # dec_value = integer_bin_string_to_dec("101010100101010")
#     # print("dec_value 5:", dec_value)
#     # dec_value = integer_bin_string_to_dec("101010101XXX101010101010")
#     # print("dec_value 6:", dec_value)
#     # dec_value = integer_bin_string_to_dec("0000000001111000000000111001")
#     # print("dec_value 7:", dec_value)
# except SICIntegerError:
#     print("A Very Bad Error Has Occurred")


# Exceptions: ValueError, IntegerOutOfRangeError
def dec_to_bin_string(dec_value: int):
    # Check for invalid input
    # Make sure dec_value is an integer
    if not isinstance(dec_value, int):
        raise SICIntegerError("Cannot convert non-integer value passed to dec_to_bin_string function")

    # Make sure dec_value is in the
    # supported range of integer values
    if not MINIMUM_INTEGER <= dec_value <= MAXIMUM_INTEGER:
        raise SICIntegerError("Integer out of range")

    is_negative = False
    if dec_value < 0:
        is_negative = True
        dec_value = abs(dec_value)

    # Convert decimal value to binary
    binary_digit_list = []
    quotient = dec_value
    while quotient != 0:
        remainder = quotient % 2
        binary_digit_list.insert(0, remainder)
        quotient = quotient // 2

    # Pad Binary Number with Zeros
    while len(binary_digit_list) < NUMBER_OF_BITS_IN_AN_INTEGER:
        binary_digit_list.insert(0, 0)

    # Check to see if 2's Complement
    # Conversion is necessary
    if is_negative:
        # Convert to 2's Complement
        # Step 1: Flip all the bits
        for index in range(NUMBER_OF_BITS_IN_AN_INTEGER):
            if binary_digit_list[index] == 0:
                binary_digit_list[index] = 1
            else:
                binary_digit_list[index] = 0

        # Step 2:  Add 1
        # carry_value = 1  # carry_value begins as the 1 that is being added
        for index in reversed(range(NUMBER_OF_BITS_IN_AN_INTEGER)):
            match binary_digit_list[index]:
                case 0:
                    binary_digit_list[index] = 1
                    break
                case 1:
                    binary_digit_list[index] = 0

    # Convert binary_digit_list to string
    binary_number_string = ""
    for binary_digit in binary_digit_list:
        binary_number_string += str(binary_digit)

    return binary_number_string


def hex_to_bin(hex_string):
    bin_string = ""

    for hex_digit in hex_string:
        bin_string += HEX_TO_BIN_DICT[hex_digit]

    return bin_string


def bin_to_hex(bin_string):
    hex_string = ""
    # Register holds 24 bits
    # range(START, STOP, STEP)
    for index in range(0, 24, 4):
        hex_string += BIN_TO_HEX_DICT[bin_string[index:index + 4]]

    return hex_string


def hex_string_to_dec(hex_string: str):
    bin_string = hex_to_bin(hex_string)

    return bin_string_to_dec(bin_string)


def dec_to_hex_string(dec_value: int):
    bin_string = dec_to_bin_string(dec_value)

    return bin_to_hex(bin_string)


# TEST BED
# try:
#     binary_value = dec_to_bin_string(-5592406)
#     print("binary_value:", binary_value)
#     binary_value = dec_to_bin_string(-5592401)
#     print("binary_value:", binary_value)
#     binary_value = dec_to_bin_string(49214)
#     print("binary_value:", binary_value)
#     binary_value = dec_to_bin_string(57)
#     print("binary_value:", binary_value)
# except SICIntegerError:
#     print("A Very Bad Error Has Occurred")
