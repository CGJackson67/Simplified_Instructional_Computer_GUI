from SIC_Utilities.sic_constants import HEX_TO_BIN_DICT, BIN_TO_HEX_DICT, INITIALIZATION_CHARACTER, BITS_IN_WORD


class SICRegisterContentsError(Exception):
    pass


class SICRegisterModel:
    NUMBER_OF_HEX_DIGITS = 6
    NUMBER_OF_BIN_DIGITS = 24

    def __init__(self, register_name):
        self.register_name = register_name
        self.hex_string = INITIALIZATION_CHARACTER * self.NUMBER_OF_HEX_DIGITS
        self.bin_string = INITIALIZATION_CHARACTER * self.NUMBER_OF_BIN_DIGITS

    def initialize_register(self):
        self.hex_string = INITIALIZATION_CHARACTER * self.NUMBER_OF_HEX_DIGITS
        self.bin_string = INITIALIZATION_CHARACTER * self.NUMBER_OF_BIN_DIGITS

    def get_register_name(self):
        return self.register_name

    def get_formatted_register_name(self):
        return self.register_name.rjust(2)

    def hex_to_bin(self, hex_string):
        bin_string = ""

        for hex_digit in hex_string:
            bin_string += HEX_TO_BIN_DICT[hex_digit]

        return bin_string

    def set_hex_string(self, hex_string):
        # Make sure hex_string contains all capital characters
        # and pad it with leading zeros if necessary
        hex_string = hex_string.upper().rjust(self.NUMBER_OF_HEX_DIGITS, "0")

        # Error check for length and hex digits
        error_found = False
        if len(hex_string) != self.NUMBER_OF_HEX_DIGITS:
            error_found = True

        for digit in hex_string:
            if digit not in HEX_TO_BIN_DICT:
                error_found = True

        if error_found:
            raise SICRegisterContentsError

        # hex_string is OK, set the value
        self.hex_string = hex_string

        # Set self.register_bin_string
        self.bin_string = self.hex_to_bin(hex_string)

    def get_hex_string(self):
        self.hex_string = self.hex_string.replace(INITIALIZATION_CHARACTER, "F")
        self.bin_string = self.bin_string.replace(INITIALIZATION_CHARACTER, "1")
        return self.hex_string

    def get_formatted_hex_string(self):
        formatted_hex_string = ""
        for index in range(len(self.hex_string)):
            if index % 2 == 0:
                formatted_hex_string += " " + self.hex_string[index]
            else:
                formatted_hex_string += self.hex_string[index]

        return formatted_hex_string.strip()

    def bin_to_hex(self, bin_string):
        hex_string = ""
        # Register holds 24 bits
        # range(START, STOP, STEP)
        for index in range(0, BITS_IN_WORD, 4):
            hex_string += BIN_TO_HEX_DICT[bin_string[index:index + 4]]

        return hex_string

    def set_bin_string(self, bin_string):
        # Pad with leading zeros if necessary
        bin_string = bin_string.rjust(self.NUMBER_OF_BIN_DIGITS, "0")

        # Error check for length and hex digits
        error_found = False
        if len(bin_string) != self.NUMBER_OF_BIN_DIGITS:
            error_found = True

        for digit in bin_string:
            if digit != "0" and digit != "1":
                error_found = True

        if error_found:
            raise SICRegisterContentsError

        # bin_string is OK, set the value
        self.bin_string = bin_string

        # Set self.register_hex_string
        # Convert bin_string to hex
        self.hex_string = self.bin_to_hex(bin_string)

    def get_bin_string(self):
        self.bin_string = self.bin_string.replace(INITIALIZATION_CHARACTER, "1")
        self.hex_string = self.hex_string.replace(INITIALIZATION_CHARACTER, "F")
        return self.bin_string

    def get_formatted_bin_string(self):
        formatted_bin_string = ""
        for index in range(len(self.bin_string)):
            if index % 8 == 0:
                formatted_bin_string += "  " + self.bin_string[index]
            elif index % 4 == 0:
                formatted_bin_string += " " + self.bin_string[index]
            else:
                formatted_bin_string += self.bin_string[index]

        return formatted_bin_string.strip()


REGISTER_A = "A"
REGISTER_X = "X"
REGISTER_L = "L"
REGISTER_PC = "PC"
REGISTER_SW = "SW"

REGISTER_DICT = {REGISTER_A: SICRegisterModel(REGISTER_A),
                 REGISTER_X: SICRegisterModel(REGISTER_X),
                 REGISTER_L: SICRegisterModel(REGISTER_L),
                 REGISTER_PC: SICRegisterModel(REGISTER_PC),
                 REGISTER_SW: SICRegisterModel(REGISTER_SW)}


def dump_registers():
    output_string = ""

    for register_name, register in REGISTER_DICT.items():
        output_string += ("REGISTER " + register.get_formatted_register_name() +
                          " :" +
                          "   HEX [" + register.get_formatted_hex_string() + "]" +
                          "   BIN [" + register.get_formatted_bin_string() + "]\n")

    print(output_string)


def initialize_registers():
    for register_name, register in REGISTER_DICT.items():
        register.initialize_register()

# TEST BED
# register_a = SICRegisterModel()
# # register_a.set_hex_string("01FDeK")
# register_a.set_bin_string("111111111000000011111111")
# # register_a.hex_to_bin(register_a.bin_to_hex("001110111111110000011110"))
# # register_a.hex_to_bin("01DEF3")
# print("bin:", register_a.get_bin_string())
# print("hex:", register_a.get_hex_string())
# register_a.set_hex_string("f180ff")
# print("bin:", register_a.get_bin_string())
# print("hex:", register_a.get_hex_string())
# register_x = SICRegisterModel()
# register_l = SICRegisterModel()
# register_pc = SICRegisterModel()
# register_sw = SICRegisterModel()
