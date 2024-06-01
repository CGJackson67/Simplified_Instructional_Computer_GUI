import os
import sys

from SIC_Peripherals.sic_output_device_05 import initialize_output_device_05
from SIC_Simulator.sic_assembly_listing_parser import sic_assembly_listing_parser, print_assembly_listing_line
from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Simulator.sic_loader import load_program_object_code
from SIC_Simulator.sic_memory_model import MEMORY_MODEL
from SIC_Simulator.sic_object_code_parser import sic_object_code_parser
from SIC_Simulator.sic_operation_executor import execute_operation
from SIC_Simulator.sic_register_model import REGISTER_DICT, dump_registers, REGISTER_PC, initialize_registers
from SIC_Utilities.sic_constants import SIC_OBJECT_CODE_FILE_EXTENSION, SIC_ASSEMBLY_LISTING_FILE_EXTENSION
from SIC_Utilities.sic_messaging import print_status, print_error


class SICSimulatorError(Exception):
    pass


# This function is used to verify the existence of
# a program object file (*.obj) and its corresponding
# assembly listing file.  If the files exist, they are
# opened for reading
def verify_and_open_program_files(program_file_name):
    program_file_dict = {}
    object_code_file_name = "." + SIC_OBJECT_CODE_FILE_EXTENSION
    assembly_listing_file_name = "." + SIC_ASSEMBLY_LISTING_FILE_EXTENSION

    # Check to see if file name includes a file extension and
    # verify that the file extension matches SIC_OBJECT_CODE_FILE_EXTENSION
    token_list = program_file_name.split(".")
    if len(token_list) == 1:
        object_code_file_name = token_list[0].strip() + object_code_file_name
        assembly_listing_file_name = token_list[0].strip() + assembly_listing_file_name
    elif len(token_list) == 2:
        if token_list[1].strip() == SIC_OBJECT_CODE_FILE_EXTENSION:
            object_code_file_name = token_list[0].strip() + object_code_file_name
            assembly_listing_file_name = token_list[0].strip() + assembly_listing_file_name
        else:
            raise SICSimulatorError("Invalid file extension")
    else:
        raise SICSimulatorError("Invalid file name")

    # Build an object code file path using the configured default working directory
    object_code_file_path = SIC_DEFAULT_WORKING_DIRECTORY + object_code_file_name

    # Check to see if the object code file exists
    if os.path.exists(object_code_file_path):
        # Open the file in read mode
        object_code_file = open(object_code_file_path, "rt")

        program_file_dict["object_code_file"] = object_code_file
    else:
        raise SICSimulatorError("Object code file does not exist\n" + object_code_file_path)

    # Build an assembly listing file path using the configured default working directory
    assembly_listing_file_path = SIC_DEFAULT_WORKING_DIRECTORY + assembly_listing_file_name

    # Check to see if the object code file exists
    if os.path.exists(assembly_listing_file_path):
        # Open the file in read mode
        assembly_listing_file = open(assembly_listing_file_path, "rt")

        program_file_dict["assembly_listing_file"] = assembly_listing_file
    else:
        raise SICSimulatorError("Assembly listing file does not exist\n" + assembly_listing_file_path)

    # Return the program file dictionary
    return program_file_dict


##########################
# SIC SIMULATOR RUNNABLE #
##########################

LOAD_MENU = "(l)oad, (q)uit"
RUN_MENU = "(s)tep, (d)ump, (r)un, (e)nd"
SIC_PROMPT = "SIC> "
END_CONFIRM = "Are you sure you want to end program? (y)es, (n)o"
QUIT_CONFIRM = "Are you sure you want to quit? (y)es, (n)o"
UNRECOGNIZED_COMMAND = "Unrecognized command"

parsed_object_code_dict_list = []
parsed_assembly_listing_dict = {}

mode = "LOAD"

print("SIC SIMULATOR")

while True:
    while mode == "LOAD":
        print(LOAD_MENU)
        command = input(SIC_PROMPT)

        match command.strip().upper():
            case "L":
                try:
                    print("Enter program file name")
                    program_file_name = input(SIC_PROMPT)

                    # Verify and open program files
                    program_file_dict = verify_and_open_program_files(program_file_name)

                    # Parse object code and assembly listing files
                    parsed_object_code_dict_list = sic_object_code_parser(program_file_dict["object_code_file"])
                    parsed_assembly_listing_dict = sic_assembly_listing_parser(
                        program_file_dict["assembly_listing_file"])

                    # Initialize memory and load program into memory
                    load_program_object_code(parsed_object_code_dict_list)

                    # Initialize registers
                    initialize_registers()

                    # Initialize the program counter register
                    header_record_dict = parsed_object_code_dict_list[0]
                    REGISTER_DICT[REGISTER_PC].set_hex_string(header_record_dict["program_start_address"])

                    # Initialize output peripheral
                    initialize_output_device_05()

                    # STATUS
                    print_status(program_file_name + " loaded and ready to run")
                    mode = "RUN"
                except SICSimulatorError as ex:
                    print_error(str(ex))
            case "Q":
                print(QUIT_CONFIRM)
                command = input(SIC_PROMPT)
                if command.strip().upper() == "Y":
                    sys.exit()
            case _:
                print(UNRECOGNIZED_COMMAND)

    while mode == "RUN":
        print(RUN_MENU)
        command = input(SIC_PROMPT)

        match command.strip().upper():
            case "S":
                print_assembly_listing_line(parsed_assembly_listing_dict, REGISTER_DICT[REGISTER_PC])
                continue_execution = execute_operation(REGISTER_DICT, MEMORY_MODEL)
                dump_registers()
                if not continue_execution:
                    mode = "LOAD"
            case "D":
                MEMORY_MODEL.dump_memory()
            case "R":
                continue_execution = True

                while continue_execution:
                    print_assembly_listing_line(parsed_assembly_listing_dict, REGISTER_DICT[REGISTER_PC])
                    continue_execution = execute_operation(REGISTER_DICT, MEMORY_MODEL)
                    dump_registers()

                MEMORY_MODEL.dump_memory()

                mode = "LOAD"
            case "E":
                print(END_CONFIRM)
                command = input(SIC_PROMPT)
                if command.strip().upper() == "Y":
                    mode = "LOAD"
            case _:
                print(UNRECOGNIZED_COMMAND)
