import random

from SIC_Peripherals.sic_input_device_F1 import read_byte_input_device_F1, test_input_device_F1
from SIC_Peripherals.sic_output_device_05 import test_output_device_05, write_byte_to_output_device_05
from SIC_Simulator.sic_memory_model import SICMemoryModelError
from SIC_Simulator.sic_register_model import REGISTER_DICT, REGISTER_A, REGISTER_PC, REGISTER_X, REGISTER_SW, REGISTER_L
from SIC_Utilities import sic_integer
from SIC_Utilities.sic_constants import HEX_TO_OPCODE_DICT, BYTES_IN_WORD, \
    FROM_INDEXED_ADDRESSING_DICT, MINIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_MEMORY_ADDRESS_DEC, MINIMUM_INTEGER, \
    MAXIMUM_INTEGER, SW_LESS_THAN, SW_EQUAL, SW_GREATER_THAN, BITS_IN_WORD
from SIC_Utilities.sic_converter import hex_string_to_dec, dec_to_hex_string, hex_word_to_bin_word
from SIC_Utilities.sic_messaging import print_error, print_status


# This function will test to see if a memory
# address is in the range of 0000 to 7FFF
def test_for_hex_memory_address_in_range(memory_address_hex_string):
    is_memory_address_in_range = False

    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    if MINIMUM_MEMORY_ADDRESS_DEC <= memory_address_dec_value <= MAXIMUM_MEMORY_ADDRESS_DEC:
        is_memory_address_in_range = True

    return is_memory_address_in_range


# This function checks to see if indexed addressing is
# called for by checking the indexed addressing flag which
# is indicated by the [X] in the instruction format below...
# INSTRUCTION FORMAT: [OPCODE 8 bits][X][ADDRESS 15 bits]
# NOTE: ELABORATE ON THIS TO CLARIFY
def test_for_indexed_addressing(memory_address_hex_string):
    is_indexed_addressing = False

    indexed_addressing_flag_character = memory_address_hex_string[0]

    if indexed_addressing_flag_character > "7":
        is_indexed_addressing = True

    return is_indexed_addressing


# This function removes t
def create_indexed_address(memory_address_hex_string, REGISTER_DICT):
    indexed_addressing_flag_character = memory_address_hex_string[0]

    # Remove the indexed addressing flag from
    # the indexed addressing flag character
    unflagged_character = FROM_INDEXED_ADDRESSING_DICT[indexed_addressing_flag_character]

    memory_address_hex_string = unflagged_character + memory_address_hex_string[1:]
    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    x_register_hex_string = REGISTER_DICT[REGISTER_X].get_hex_string()
    x_register_dec_value = hex_string_to_dec(x_register_hex_string)

    memory_address_hex_string = dec_to_hex_string(memory_address_dec_value + x_register_dec_value)

    return memory_address_hex_string


# This function
def execute_operation(REGISTER_DICT, MEMORY_MODEL):
    # PROGRAM COUNTER
    pc_register_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_PC].get_hex_string())

    # OPCODE
    # Look up operation code in memory and validate
    try:
        opcode_hex_string = MEMORY_MODEL.get_byte(pc_register_dec_value)
    except SICMemoryModelError:
        print_error("MEMORY FAULT: Halting program execution\n")
        continue_execution = False
        return continue_execution

    opcode_mnemonic = HEX_TO_OPCODE_DICT.get(opcode_hex_string)

    # Verify that opcode is supported
    if opcode_mnemonic is None:
        print_error("UNRECOGNIZED OPCODE FAULT: Halting program execution",
                    "OPCODE: " + opcode_hex_string + "\n")
        continue_execution = False
        return continue_execution

    # MEMORY ADDRESS
    # Build the memory address
    try:
        memory_address_hex_string = MEMORY_MODEL.get_bytes(pc_register_dec_value + 1, 2)
    except SICMemoryModelError:
        print_error("MEMORY FAULT: Halting program execution\n")
        continue_execution = False
        return continue_execution

    # Test for indexed addressing
    is_indexed_addressing = test_for_indexed_addressing(memory_address_hex_string)

    if is_indexed_addressing:
        memory_address_hex_string = create_indexed_address(memory_address_hex_string, REGISTER_DICT)

    memory_address_dec_value = hex_string_to_dec(memory_address_hex_string)

    # Increment PC Register
    REGISTER_DICT[REGISTER_PC].set_hex_string(dec_to_hex_string(pc_register_dec_value + BYTES_IN_WORD))
    # Verify that the Program Counter holds an in-range memory address
    if not test_for_hex_memory_address_in_range(REGISTER_DICT[REGISTER_PC].get_hex_string()):
        print_error("PROGRAM COUNTER FAULT: Halting program execution",
                    "PC REGISTER: " + REGISTER_DICT[REGISTER_PC].get_hex_string() + "\n")
        continue_execution = False
        return continue_execution

    # EXECUTE INSTRUCTION
    match opcode_mnemonic:
        case "ADD":
            # A <- (A) + (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert to decimal value and do the arithmetic
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            sum_dec_value = register_a_dec_value + word_dec_value

            if not MINIMUM_INTEGER <= sum_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(sum_dec_value))

            continue_execution = True
            return continue_execution
        case "AND":
            # A <- (A) & (m..m+2)
            # Get the contents of register a as a binary string
            register_a_bin_string = REGISTER_DICT[REGISTER_A].get_bin_string()

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert hex string to bin string
            word_bin_string = hex_word_to_bin_word(word_hex_string)

            # Do the logical and
            and_bin_string = ""

            for index in range(BITS_IN_WORD):
                if register_a_bin_string[index] == "1" and word_bin_string[index] == "1":
                    and_bin_string += "1"
                else:
                    and_bin_string += "0"

            # Put the result in register a
            REGISTER_DICT[REGISTER_A].set_bin_string(and_bin_string)

            continue_execution = True
            return continue_execution
        case "COMP":
            # (A) : (m..m+2)
            # Get value held in register a
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = hex_string_to_dec(register_a_hex_string)

            # Compare the value in register a
            # with value at the memory address and set the
            # Status Word register accordingly
            try:
                memory_value_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, 3)
                memory_value_dec_value = sic_integer.hex_string_to_dec(memory_value_hex_string)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            if register_a_dec_value < memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_LESS_THAN)
            elif register_a_dec_value == memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_EQUAL)
            elif register_a_dec_value > memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_GREATER_THAN)

            continue_execution = True
            return continue_execution
        case "DIV":
            # A <- (A) / (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert to decimal value and do the arithmetic
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            if word_dec_value == 0:
                print_error("DIVISION BY ZERO ERROR FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            quotient_dec_value = register_a_dec_value // word_dec_value

            if not MINIMUM_INTEGER <= quotient_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(quotient_dec_value))

            continue_execution = True
            return continue_execution
        case "J":
            # PC <- m
            REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string.rjust(6, "0"))

            continue_execution = True
            return continue_execution
        case "JEQ":
            # PC <- m if CC set to =
            status_word = REGISTER_DICT[REGISTER_SW].get_hex_string()

            if status_word == SW_EQUAL:
                REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string)

            continue_execution = True
            return continue_execution
        case "JGT":
            # PC <- m if CC set to >
            status_word = REGISTER_DICT[REGISTER_SW].get_hex_string()

            if status_word == SW_GREATER_THAN:
                REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string)

            continue_execution = True
            return continue_execution
        case "JLT":
            # PC <- m if CC set to <>>
            status_word = REGISTER_DICT[REGISTER_SW].get_hex_string()

            if status_word == SW_LESS_THAN:
                REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string)

            continue_execution = True
            return continue_execution
        case "JSUB":
            # L <- (PC); PC <- m
            # Store the program counter in register l
            pc_register_hex_string = REGISTER_DICT[REGISTER_PC].get_hex_string()
            REGISTER_DICT[REGISTER_L].set_hex_string(pc_register_hex_string)

            # Store the memory address in the program counter
            REGISTER_DICT[REGISTER_PC].set_hex_string(memory_address_hex_string.rjust(6, "0"))

            continue_execution = True
            return continue_execution
        case "LDA":
            # A <- (m..m+2)
            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(word_hex_string)

            continue_execution = True
            return continue_execution
        case "LDCH":
            # A[rightmost byte] <- (m)
            # All other bytes in register a remain unchanged
            # Get the byte value at the indicated memory location
            try:
                byte_string = MEMORY_MODEL.get_byte(memory_address_dec_value)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Set the rightmost byte in register a
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_hex_string = register_a_hex_string[:4] + byte_string
            REGISTER_DICT[REGISTER_A].set_hex_string(register_a_hex_string)

            continue_execution = True
            return continue_execution
        case "LDL":
            # L <- (m..m+2)
            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_L].set_hex_string(word_hex_string)

            continue_execution = True
            return continue_execution
        case "LDX":
            # X <- (m..m+2)
            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_X].set_hex_string(word_hex_string)

            continue_execution = True
            return continue_execution
        case "MUL":
            # A <- (A) * (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert to decimal value and do the arithmetic
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            product_dec_value = register_a_dec_value * word_dec_value

            if not MINIMUM_INTEGER <= product_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(product_dec_value))

            continue_execution = True
            return continue_execution
        case "OR":
            # A <- (A) | (m..m+2)
            # Get the contents of register a as a binary string
            register_a_bin_string = REGISTER_DICT[REGISTER_A].get_bin_string()

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert hex string to bin string
            word_bin_string = hex_word_to_bin_word(word_hex_string)

            # Do the logical and
            and_bin_string = ""

            for index in range(BITS_IN_WORD):
                if register_a_bin_string[index] == "0" and word_bin_string[index] == "0":
                    and_bin_string += "0"
                else:
                    and_bin_string += "1"

            # Put the result in register a
            REGISTER_DICT[REGISTER_A].set_bin_string(and_bin_string)

            continue_execution = True
            return continue_execution
        case "RD":
            # A[rightmost byte] <- data from device specified by (m)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_x_hex_string = REGISTER_DICT[REGISTER_X].get_hex_string()

            is_in_EOF_state = False
            if register_a_hex_string == "000000" and register_x_hex_string == "000000":
                is_in_EOF_state = True

            byte_string = read_byte_input_device_F1(is_in_EOF_state)

            register_a_hex_string = register_a_hex_string[:4] + byte_string
            REGISTER_DICT[REGISTER_A].set_hex_string(register_a_hex_string)

            continue_execution = True
            return continue_execution
        case "RSUB":
            # PC <- (L)
            REGISTER_DICT[REGISTER_PC].set_hex_string(REGISTER_DICT[REGISTER_L].get_hex_string())

            # Verify that the Program Counter holds an in-range memory address
            if not test_for_hex_memory_address_in_range(REGISTER_DICT[REGISTER_PC].get_hex_string()):
                print_error("PROGRAM COUNTER FAULT: Halting program execution",
                            "PC REGISTER: " + REGISTER_DICT[REGISTER_PC].get_hex_string() + "\n")
                continue_execution = False
                return continue_execution

            continue_execution = True
            return continue_execution
        case "STA":
            # m..m+2 <- (A)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()

            index = 0
            start_index = 0
            end_index = 2
            while index < BYTES_IN_WORD:
                try:
                    MEMORY_MODEL.set_byte(memory_address_dec_value + index,
                                          register_a_hex_string[start_index:end_index])
                except SICMemoryModelError:
                    print_error("MEMORY FAULT: Halting program execution\n")
                    continue_execution = False
                    return continue_execution
                index += 1
                start_index += 2
                end_index += 2

            continue_execution = True
            return continue_execution
        case "STCH":
            # m <- (A)[rightmost byte]
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            byte_string = register_a_hex_string[4:]
            try:
                MEMORY_MODEL.set_byte(memory_address_dec_value, byte_string)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            continue_execution = True
            return continue_execution
        case "STL":
            # m..m+2 <- (L)
            register_l_hex_string = REGISTER_DICT[REGISTER_L].get_hex_string()

            index = 0
            start_index = 0
            end_index = 2
            while index < BYTES_IN_WORD:
                try:
                    MEMORY_MODEL.set_byte(memory_address_dec_value + index,
                                          register_l_hex_string[start_index:end_index])
                except SICMemoryModelError:
                    print_error("MEMORY FAULT: Halting program execution\n")
                    continue_execution = False
                    return continue_execution
                index += 1
                start_index += 2
                end_index += 2

            continue_execution = True
            return continue_execution
        case "STSW":
            # m..m+2 <- (SW)
            register_sw_hex_string = REGISTER_DICT[REGISTER_SW].get_hex_string()

            index = 0
            start_index = 0
            end_index = 2
            while index < BYTES_IN_WORD:
                try:
                    MEMORY_MODEL.set_byte(memory_address_dec_value + index,
                                          register_sw_hex_string[start_index:end_index])
                except SICMemoryModelError:
                    print_error("MEMORY FAULT: Halting program execution\n")
                    continue_execution = False
                    return continue_execution
                index += 1
                start_index += 2
                end_index += 2

            continue_execution = True
            return continue_execution
        case "STX":
            register_x_hex_string = REGISTER_DICT[REGISTER_X].get_hex_string()

            index = 0
            start_index = 0
            end_index = 2
            while index < BYTES_IN_WORD:
                try:
                    MEMORY_MODEL.set_byte(memory_address_dec_value + index,
                                          register_x_hex_string[start_index:end_index])
                except SICMemoryModelError:
                    print_error("MEMORY FAULT: Halting program execution\n")
                    continue_execution = False
                    return continue_execution
                index += 1
                start_index += 2
                end_index += 2

            continue_execution = True
            return continue_execution
        case "SUB":
            # A <- (A) - (m..m+2)
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            register_a_dec_value = sic_integer.hex_string_to_dec(register_a_hex_string)

            # Build the value held at the indicated memory location
            try:
                word_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, BYTES_IN_WORD)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            # Convert to decimal value and do the arithmetic
            word_dec_value = sic_integer.hex_string_to_dec(word_hex_string)

            difference_dec_value = register_a_dec_value - word_dec_value

            if not MINIMUM_INTEGER <= difference_dec_value <= MAXIMUM_INTEGER:
                print_error("INTEGER OUT OF RANGE FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            REGISTER_DICT[REGISTER_A].set_hex_string(sic_integer.dec_to_hex_string(difference_dec_value))

            continue_execution = True
            return continue_execution
        case "TD":
            # Test device specified by (m)
            # Determine which device to test
            try:
                byte_string = MEMORY_MODEL.get_byte(memory_address_dec_value)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            match byte_string:
                case "05":
                    test_device_response_hex_string = test_output_device_05()
                case "F1":
                    test_device_response_hex_string = test_input_device_F1()
                case _:
                    print_error("PERIPHERAL DEVICE FAULT: Halting program execution\n")
                    continue_execution = False
                    return continue_execution

            # Set Status Word to the test device response
            REGISTER_DICT[REGISTER_SW].set_hex_string(test_device_response_hex_string)

            continue_execution = True
            return continue_execution
        case "TIX":
            # X <- (X) + 1; (X) : (m..m+2)
            # Increment the value in the x register
            register_x_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_X].get_hex_string()) + 1
            register_x_hex_string = dec_to_hex_string(register_x_dec_value)
            REGISTER_DICT[REGISTER_X].set_hex_string(register_x_hex_string)

            # Compare the incremented value in register x
            # with value at the memory address and set the
            # Status Word register accordingly
            try:
                memory_value_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, 3)
                memory_value_dec_value = sic_integer.hex_string_to_dec(memory_value_hex_string)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            if register_x_dec_value < memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_LESS_THAN)
            elif register_x_dec_value == memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_EQUAL)
            elif register_x_dec_value > memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_GREATER_THAN)

            continue_execution = True
            return continue_execution
        case "WD":
            # Device specified by (m) <- (A)[rightmost byte]
            register_a_hex_string = REGISTER_DICT[REGISTER_A].get_hex_string()
            byte_string = register_a_hex_string[4:]
            write_byte_to_output_device_05(byte_string)

            continue_execution = True
            return continue_execution
        case "XOS":
            # End processing and exit to the operating system
            print_status("Program execution terminated normally\n")
            continue_execution = False
            return continue_execution
        case "TIXB":
            # X <- (X) + 1; (X) : (m..m+2)
            # Increment the value in the x register
            # NOTE: Function identical to TIX
            register_x_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_X].get_hex_string()) + 1
            register_x_hex_string = dec_to_hex_string(register_x_dec_value)
            REGISTER_DICT[REGISTER_X].set_hex_string(register_x_hex_string)

            # Compare the incremented value in register x
            # with value at the memory address and set the
            # Status Word register accordingly
            try:
                memory_value_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, 3)
                memory_value_dec_value = sic_integer.hex_string_to_dec(memory_value_hex_string)
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            if register_x_dec_value < memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_LESS_THAN)
            elif register_x_dec_value == memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_EQUAL)
            elif register_x_dec_value > memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_GREATER_THAN)

            continue_execution = True
            return continue_execution
        case "TIXW":
            # X <- (X) + 3; (X) : ((m..m+2) * 3)
            # Increment the value in the x register
            register_x_dec_value = hex_string_to_dec(REGISTER_DICT[REGISTER_X].get_hex_string()) + 3
            register_x_hex_string = dec_to_hex_string(register_x_dec_value)
            REGISTER_DICT[REGISTER_X].set_hex_string(register_x_hex_string)

            # Compare the incremented value in register x
            # with value at the memory address * 3 bytes (one word)
            # and set the Status Word register accordingly
            try:
                memory_value_hex_string = MEMORY_MODEL.get_bytes(memory_address_dec_value, 3)
                memory_value_dec_value = sic_integer.hex_string_to_dec(memory_value_hex_string) * 3
            except SICMemoryModelError:
                print_error("MEMORY FAULT: Halting program execution\n")
                continue_execution = False
                return continue_execution

            if register_x_dec_value < memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_LESS_THAN)
            elif register_x_dec_value == memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_EQUAL)
            elif register_x_dec_value > memory_value_dec_value:
                REGISTER_DICT[REGISTER_SW].set_hex_string(SW_GREATER_THAN)

            continue_execution = True
            return continue_execution
