import os

from SIC_Assembler.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_GUI.Assembler.assembly_status_panel import AssemblyStatusPanel
from SIC_Utilities import sic_integer
from SIC_Utilities.sic_constants import MAXIMUM_MEMORY_ADDRESS_DEC, MAXIMUM_NUMBER_OF_LABELS, LOC_COLUMN_WIDTH, \
    LABEL_COLUMN_WIDTH, OPCODE_COLUMN_WIDTH, OPERAND_COLUMN_WIDTH, OBJECT_CODE_COLUMN_WIDTH, OPCODE_TO_HEX_DICT, \
    TO_INDEXED_ADDRESSING_DICT, OBJECT_CODE_TEXT_RECORD_BODY_LENGTH, SIC_ASSEMBLY_CODE_FILE_EXTENSION
from SIC_Utilities.sic_converter import hex_string_to_dec, dec_to_memory_address_hex_string, dec_to_hex_string
from SIC_Utilities.sic_messaging import print_status

# GLOBALS
label_dict = {}
program_length_dec = 0


class SICAssemblerError(Exception):
    pass


# This function determines the number of
# bytes  requested from a BYTE operand
def get_byte_assembly_directive_byte_count(operand_string):
    if operand_string[0] == "X":
        # Handle hex
        return len(operand_string[2:-1]) // 2
    else:
        # Handle characters
        return len(operand_string[2:-1])


# This function does pass 1 of a two-pass assembly
# 1) Assign addresses to all statements in the assembly program
# 2) Store the addresses assigned to labels for use in Pass 2 processing
def assembler_pass_one(parsed_code_dict_list, assembly_status_panel: AssemblyStatusPanel):
    # ASSEMBLER PASS ONE
    # STATUS
    status_message = "Beginning pass one assembly"
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")

    # Initialize the label dictionary
    global label_dict
    label_dict = {}

    location_counter_dec = 0
    start_address_dec = location_counter_dec

    for line_of_code_dict in parsed_code_dict_list:
        # DEBUG
        # print(line_of_code_dict)

        # Check for comment line and ignore
        if line_of_code_dict["comment"]:
            continue

        # Check for START opcode and process
        if line_of_code_dict["opcode"] == "START":
            location_counter_hex_string = line_of_code_dict["operand"]
            location_counter_dec = hex_string_to_dec(location_counter_hex_string)
            start_address_dec = location_counter_dec
        # Process all other opcodes
        else:
            # Handle label
            label = line_of_code_dict.get("label")

            if label is not None:
                if label_dict.get(label) is None:
                    if len(label_dict) < MAXIMUM_NUMBER_OF_LABELS:
                        label_dict[label] = dec_to_memory_address_hex_string(location_counter_dec)
                    else:
                        # ERROR
                        raise SICAssemblerError("Maximum number of LABELS exceeded\n" +
                                                "LINE " + str(line_of_code_dict["line_number"]) + ": " +
                                                line_of_code_dict["unparsed_line_of_code"])
                else:
                    # ERROR
                    raise SICAssemblerError("Duplicate LABEL found\n" +
                                            "LINE " + str(line_of_code_dict["line_number"]) + ": " +
                                            line_of_code_dict["unparsed_line_of_code"])

            # Record current location counter
            line_of_code_dict["location_counter"] = dec_to_memory_address_hex_string(location_counter_dec)

            # Increment location counter as required
            match line_of_code_dict["opcode"]:
                case "WORD":
                    location_counter_dec += 3
                case "RESW":
                    location_counter_dec += 3 * int(line_of_code_dict["operand"])
                case "RESB":
                    location_counter_dec += int(line_of_code_dict["operand"])
                case "BYTE":
                    location_counter_dec += get_byte_assembly_directive_byte_count(line_of_code_dict["operand"])
                case "END":
                    # Location counter not used with the END operand
                    line_of_code_dict.pop("location_counter")
                    global program_length_dec
                    program_length_dec = location_counter_dec - start_address_dec
                    # DEBUG
                    # print("Program length DEC:", program_length_dec,
                    #       "HEX:", dec_to_hex_string(program_length_dec))
                    break
                case _:
                    location_counter_dec += 3

            if location_counter_dec > MAXIMUM_MEMORY_ADDRESS_DEC:
                # ERROR
                raise SICAssemblerError("Location Counter out of range\n" +
                                        "LINE " + str(line_of_code_dict["line_number"]) + ": " +
                                        line_of_code_dict["unparsed_line_of_code"])

            # DEBUG
            # print(line_of_code_dict)

    # DEBUG
    # print("LABEL DICTIONARY:", label_dict)

    # STATUS
    status_message = "Pass one assembly complete"
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")


# This function formats assembly listing columns
# by adding the required number of spaces to the
# of the code token string
def format_assembly_listing_column(code_token, column_width):
    if code_token is None:
        code_token = ""

    spaces_to_add = column_width - len(code_token)

    return code_token + " " * spaces_to_add


# This function creates the object code associated
# with a BYTE opcode in the line of code dictionary
def create_object_code_for_byte(line_of_code_dict):
    object_code = ""

    operand = line_of_code_dict["operand"]

    if operand[0] == "C":
        # Handle ascii characters
        character_list = list(operand[2:-1])

        for character in character_list:
            ascii_dec = ord(character)
            ascii_hex = dec_to_hex_string(ascii_dec)
            object_code += ascii_hex
    elif operand[0] == "X":
        # Handle hex values
        object_code = operand[2:-1]

    return object_code


# This function creates the object code associated
# with a WORD opcode in the line of code dictionary
def create_object_code_for_word(line_of_code_dict):
    OBJECT_CODE_LENGTH = 6
    object_code = ""

    operand = line_of_code_dict["operand"]

    object_code = sic_integer.dec_to_hex_string(int(operand))

    # Pad object with leading zeros if necessary
    while len(object_code) < OBJECT_CODE_LENGTH:
        object_code = "0" + object_code

    return object_code


# This function creates the object code associated
# with all other opcodes in the line of code
# dictionary that require object code
def create_object_code(line_of_code_dict, label_dict):
    object_code = ""

    opcode = line_of_code_dict.get("opcode")
    operand = line_of_code_dict.get("operand")

    opcode_hex = OPCODE_TO_HEX_DICT[opcode]

    if operand is None:
        # Handle RSUB
        object_code = opcode_hex + "0000"
    elif operand[0] == "0":
        # Handle memory address
        object_code = opcode_hex + operand[1:]
    else:
        # Handle labels
        memory_address = label_dict.get(operand)

        if memory_address is not None:
            object_code = opcode_hex + memory_address
        else:
            raise SICAssemblerError("Undefined label encountered")

    if line_of_code_dict["indexed_addressing"]:
        object_code_list = list(object_code)
        object_code_list[2] = TO_INDEXED_ADDRESSING_DICT[object_code_list[2]]
        object_code = ""
        for character in object_code_list:
            object_code += character

    return object_code


# This function creates a line for the assembly listing file
# based upon the parsed contents of a line of code dictionary
def create_assembly_listing_line(line_of_code_dict):
    assembly_listing_line = ""

    # Format location counter column
    loc = line_of_code_dict.get("location_counter")
    assembly_listing_line += format_assembly_listing_column(loc, LOC_COLUMN_WIDTH)

    # Format label column
    label = line_of_code_dict.get("label")
    assembly_listing_line += format_assembly_listing_column(label, LABEL_COLUMN_WIDTH)

    # Format opcode column
    opcode = line_of_code_dict.get("opcode")
    assembly_listing_line += format_assembly_listing_column(opcode, OPCODE_COLUMN_WIDTH)

    # Format operand column
    operand = line_of_code_dict.get("operand")
    if line_of_code_dict["indexed_addressing"]:
        operand = operand + ",X"
    assembly_listing_line += format_assembly_listing_column(operand, OPERAND_COLUMN_WIDTH)

    # Format object code column
    object_code = line_of_code_dict.get("object_code")
    assembly_listing_line += format_assembly_listing_column(object_code, OBJECT_CODE_COLUMN_WIDTH)

    return assembly_listing_line + "\n"


# The function creates a new object code text record header
def create_object_code_text_record_header(location_counter):
    return "T00" + location_counter


# The function creates an object code text record properly
# formatted and ready to write to the object code file
def create_object_code_text_record(object_code_text_record_header, object_code_text_record_body):
    body_byte_count = len(object_code_text_record_body) // 2
    object_code_text_record_byte_count = dec_to_hex_string(body_byte_count)
    # Return the properly formatted text record
    return (object_code_text_record_header +
            object_code_text_record_byte_count.rjust(2, "0") +
            object_code_text_record_body +
            "\n")


# This function does pass 2 of a two-pass assembly
# 1) Assemble instructions by translating opcodes and looking up addresses
# 2) Generate data values defined by BYTE, WORD, RESB, RESW
# 3) Perform any needed processing of assembly directives not done in pass 1
# 4) Write the object code file and the assembly listing file
def assembler_pass_two(parsed_code_dict_list, assembly_code_file_path, assembly_status_panel: AssemblyStatusPanel):
    # ASSEMBLER PASS TWO
    # STATUS
    status_message = "Beginning pass two assembly"
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")

    # Initialize starting address
    start_address_hex = ""

    # Open Object Code file for writing
    object_code_file_path = assembly_code_file_path[:-3]
    object_code_file_path += "obj"

    object_code_file = open(object_code_file_path, "w")
    # STATUS
    status_message = "Object code file ready for writing\n" + object_code_file_path
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")

    # Open Assembly Listing file for writing
    assembly_listing_file_path = assembly_code_file_path[:-3]
    assembly_listing_file_path += "lst"

    assembly_listing_file = open(assembly_listing_file_path, "w")
    # STATUS
    status_message = "Assembly listing file ready for writing\n" + assembly_listing_file_path
    print_status(status_message)
    assembly_status_panel.set_assembly_status(status_message + "\n")

    # Initialize text record header and body
    object_code_text_record_header = ""
    object_code_text_record_body = ""

    for line_of_code_dict in parsed_code_dict_list:
        # DEBUG
        # print(line_of_code_dict)
        # Initialize object code
        object_code = ""
        # Handle the various opcodes
        # And generate object code
        match line_of_code_dict["opcode"]:
            case "START":
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
                # Save starting address for use by END
                start_address_hex = line_of_code_dict["operand"]
                # Create object code header record
                object_code_header_record = ("H" +
                                             line_of_code_dict["label"].ljust(6, " ") +
                                             start_address_hex.rjust(6, "0") +
                                             dec_to_hex_string(program_length_dec).rjust(6, "0") +
                                             "\n")
                # Write header record to the object code file
                object_code_file.write(object_code_header_record)
                # No further processing required, continue the for loop
                continue
            case "BYTE":
                # Create object for BYTE operand and add
                # it to the line of code dictionary
                object_code = create_object_code_for_byte(line_of_code_dict)
                line_of_code_dict["object_code"] = object_code
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
            case "WORD":
                # Create object for BYTE operand and add
                # it to the line of code dictionary
                object_code = create_object_code_for_word(line_of_code_dict)
                line_of_code_dict["object_code"] = object_code
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
            case "RESB":
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
                # Write the current text record to
                # the object code file if it exists
                if object_code_text_record_header != "":
                    object_code_file.write(create_object_code_text_record(object_code_text_record_header,
                                                                          object_code_text_record_body))
                    # Initialize new text record header and body
                    object_code_text_record_header = ""
                    object_code_text_record_body = ""
                # No further processing required, continue the for loop
                continue
            case "RESW":
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
                # Write the current text record to
                # the object code file if it exists
                if object_code_text_record_header != "":
                    object_code_file.write(create_object_code_text_record(object_code_text_record_header,
                                                                          object_code_text_record_body))
                    # Initialize new text record header and body
                    object_code_text_record_header = ""
                    object_code_text_record_body = ""
                # No further processing required, continue the for loop
                continue
            case "END":
                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)
                # Write the last text record to the object code file if it exists
                if object_code_text_record_header != "":
                    object_code_file.write(create_object_code_text_record(object_code_text_record_header,
                                                                          object_code_text_record_body))
                # Create object code end record
                object_code_end_record = ("E" +
                                          start_address_hex.rjust(6, "0") +
                                          "\n")
                # Write end record to the object code file
                object_code_file.write(object_code_end_record)

                # No further processing required, close files and exit
                object_code_file.close()
                assembly_listing_file.close()
                # STATUS
                status_message = "Object code file written and closed\n" + "Assembly listing file written and closed\n" + "Pass two assembly complete"
                print_status(status_message)
                assembly_status_panel.set_assembly_status(status_message)

                return
            case _:
                # Create object for BYTE operand and add
                # it to the line of code dictionary
                try:
                    object_code = create_object_code(line_of_code_dict, label_dict)
                    line_of_code_dict["object_code"] = object_code
                except SICAssemblerError as ex:
                    # Close object code file and assembly listing file,
                    # print error message, and exit program
                    object_code_file.close()
                    assembly_listing_file.close()
                    # ERROR
                    raise SICAssemblerError(str(ex) + "\n" +
                                            "LINE " + str(line_of_code_dict["line_number"]) + ": " +
                                            line_of_code_dict["unparsed_line_of_code"])

                # Create and write assembly listing line
                assembly_listing_line = create_assembly_listing_line(line_of_code_dict)
                assembly_listing_file.write(assembly_listing_line)

        # Create object code text record and write to the object code file
        if object_code_text_record_header == "":
            object_code_text_record_header = create_object_code_text_record_header(
                line_of_code_dict["location_counter"])

        if (len(object_code_text_record_body) + len(object_code)) <= OBJECT_CODE_TEXT_RECORD_BODY_LENGTH:
            object_code_text_record_body += object_code
        else:
            # Write object code text record to object code file
            object_code_file.write(create_object_code_text_record(object_code_text_record_header,
                                                                  object_code_text_record_body))
            # Initial a new text record
            object_code_text_record_header = create_object_code_text_record_header(
                line_of_code_dict["location_counter"])
            object_code_text_record_body = object_code


# This function is used to verify the existence of
# an assembly program file (*.asm).
def verify_program_file_path(program_file_name):
    assembly_code_file_name = "." + SIC_ASSEMBLY_CODE_FILE_EXTENSION

    # Check to see if file name includes a file extension and verify
    # that the file extension matches SIC_ASSEMBLY_CODE_FILE_EXTENSION
    token_list = program_file_name.split(".")
    if len(token_list) == 1:
        assembly_code_file_name = token_list[0].strip() + assembly_code_file_name
    elif len(token_list) == 2:
        if token_list[1].strip() == SIC_ASSEMBLY_CODE_FILE_EXTENSION:
            assembly_code_file_name = token_list[0].strip() + assembly_code_file_name
        else:
            raise SICAssemblerError("Invalid file extension")
    else:
        raise SICAssemblerError("Invalid file name")

    # Build an assembly code file path using the configured default working directory
    assembly_code_file_path = SIC_DEFAULT_WORKING_DIRECTORY + assembly_code_file_name

    # Check to see if the assembly code file exists
    if os.path.exists(assembly_code_file_path):

        return assembly_code_file_path
    else:
        raise SICAssemblerError("Assembly program file does not exist\n" + assembly_code_file_path)


##########################
# SIC ASSEMBLER RUNNABLE #
##########################

# SICASM_PROMPT = "SICASM> "
# ASSEMBLE_MENU = "(a)ssemble, (q)uit"
# QUIT_CONFIRM = "Are you sure you want to quit? (y)es, (n)o"
# UNRECOGNIZED_COMMAND = "Unrecognized command"
#
# print("SIC ASSEMBLER")
#
# while True:
#     print(ASSEMBLE_MENU)
#     command = input(SICASM_PROMPT)
#
#     match command.strip().upper():
#         case "A":
#             try:
#                 print("Enter program file name")
#                 program_file_name = input(SICASM_PROMPT)
#
#                 # Verify program file path
#                 program_file_path = verify_program_file_path(program_file_name)
#
#                 # Parse assembly code
#                 parsed_code_dict_list = parse_assembly_code_file(program_file_path)
#
#                 # Execute pass one and pass two assembly
#                 assembler_pass_one(parsed_code_dict_list)
#                 assembler_pass_two(parsed_code_dict_list, program_file_path)
#             except (SICAssemblyParserError, SICAssemblerError) as ex:
#                 # ERROR
#                 print_error(str(ex))
#         case "Q":
#             print(QUIT_CONFIRM)
#             command = input(SICASM_PROMPT)
#             if command.strip().upper() == "Y":
#                 sys.exit()
#         case _:
#             print(UNRECOGNIZED_COMMAND)

# TEST BED
# Create path to assembly code file.
# NOTE: File should be indicated at run time
# assembly_code_file_name = "ReadWrite.asm"
# assembly_code_file_name = "Sum.asm"
# assembly_code_file_name = "SumModified.asm"
# assembly_code_file_name = "ReadWriteTEST01.asm"
# assembly_code_file_name = "ReadWriteTEST02.asm"
# assembly_code_file_path = ("C:\\Users\\Chris Jackson\\PycharmProjects\\SIC_System_Software\\Assembly Code\\" +
#                            assembly_code_file_name)
#
# parsed_code_dict_list = parse_assembly_code_file(assembly_code_file_path)
#
# assembler_pass_one(parsed_code_dict_list)
#
# assembler_pass_two(parsed_code_dict_list, assembly_code_file_path)
