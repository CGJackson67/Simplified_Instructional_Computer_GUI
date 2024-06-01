import os.path

from SIC_Simulator.sic_configuration import SIC_DEFAULT_WORKING_DIRECTORY
from SIC_Utilities.sic_constants import SIC_OBJECT_CODE_FILE_EXTENSION
from SIC_Utilities.sic_converter import test_for_hex, hex_string_to_dec
from SIC_Utilities.sic_messaging import print_error, print_status


class SICObjectCodeParserError(Exception):
    pass


# This function parses a header record from
# the object code file.  It stores record type,
# program name, program start address, program length, and
# the unparsed end record. in a line of code dictionary
def parse_header_record(unparsed_line_of_object_code):
    # Validate the unparsed line of code
    # Make sure header record is 19 characters long
    # Verify that from characters 7-19 are hex characters
    if (len(unparsed_line_of_object_code) == 19 and
            test_for_hex(unparsed_line_of_object_code[7:])):

        parsed_line_object_code_dict = {"record_type": "header",
                                        "program_name": unparsed_line_of_object_code[1:7].rstrip(),
                                        "program_start_address": unparsed_line_of_object_code[9:13],
                                        "program_length": unparsed_line_of_object_code[15:19],
                                        "unparsed_line_of_object_code": unparsed_line_of_object_code}

        return parsed_line_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid header record")


# This function parses a text record from
# the object code file.  It stores record type,
# start address, byte count, byte list,  and the
# unparsed end record. in a line of code dictionary
def parse_text_record(unparsed_line_of_object_code):
    # Validate the unparsed line of code
    # Make sure header record is 11-69 characters long
    # Verify that object contains an even number of characters
    # Verify that the object code is made up of hex characters
    if (11 <= len(unparsed_line_of_object_code) <= 69 and
            len(unparsed_line_of_object_code[1:]) % 2 == 0 and
            test_for_hex(unparsed_line_of_object_code[1:])):

        byte_list = []
        byte_object_code = unparsed_line_of_object_code[9:]

        start_index = 0
        end_index = 2

        while end_index <= len(byte_object_code):
            byte_list.append(byte_object_code[start_index:end_index])

            start_index += 2
            end_index += 2

        # Verify that byte count is correct
        byte_count = unparsed_line_of_object_code[7:9]
        if hex_string_to_dec(byte_count) != len(byte_list):
            # ERROR
            raise SICObjectCodeParserError("Invalid text record")

        parsed_line_object_code_dict = {"record_type": "text",
                                        "start_address": unparsed_line_of_object_code[3:7],
                                        "byte_count": byte_count,
                                        "byte_list": byte_list,
                                        "unparsed_line_of_object_code": unparsed_line_of_object_code}

        return parsed_line_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid text record")


# This function parses an end record from
# the object code file.  It stores record type,
# program start address, and the unparsed end record.
# in a line of code dictionary
def parse_end_record(unparsed_line_of_object_code):
    # Validate the unparsed line of code
    # Make sure header record is 7 characters long
    # Verify that from characters 2-7 are hex characters
    if (len(unparsed_line_of_object_code) == 7 and
            test_for_hex(unparsed_line_of_object_code[1:])):

        parsed_line_object_code_dict = {"record_type": "end",
                                        "program_start_address": unparsed_line_of_object_code[3:7],
                                        "unparsed_line_of_object_code": unparsed_line_of_object_code}

        return parsed_line_object_code_dict

    else:
        # ERROR
        raise SICObjectCodeParserError("Invalid end record")


# This function reads an object code file (*.obj).
# It processes each line of code one at a time.
# It parses out all the relevant object code tokens
# for header, text, and end records and then
# stores them in a line of code dictionary.
# It returns a list containing all the parsed line of code
# dictionaries.
def sic_object_code_parser(object_code_file):
    parsed_object_code_dict_list = []

    header_found = False
    end_found = False

    for line_of_object_code in object_code_file:
        # Remove newline and any other trailing whitespaces
        unparsed_line_of_object_code = line_of_object_code.rstrip()

        record_type_indicator = line_of_object_code[0]

        try:
            match record_type_indicator:
                case "H":
                    parsed_object_code_dict_list.append(parse_header_record(unparsed_line_of_object_code))
                case "T":
                    parsed_object_code_dict_list.append(parse_text_record(unparsed_line_of_object_code))
                case "E":
                    parsed_object_code_dict_list.append(parse_end_record(unparsed_line_of_object_code))
                case _:
                    # ERROR
                    raise SICObjectCodeParserError("Invalid record type")

        except SICObjectCodeParserError as ex:
            object_code_file.close()
            # ERROR
            raise SICObjectCodeParserError("Could not parse object code file - " + str(ex))

    object_code_file.close()

    return parsed_object_code_dict_list

# TEST BED
# object_code_file_name = "ReadWrite"
#
# object_code_file_path = (SIC_DEFAULT_WORKING_DIRECTORY +
#                          object_code_file_name + "." +
#                          SIC_OBJECT_CODE_FILE_EXTENSION)
#
# object_code_file = open(object_code_file_path, "rt")
#
#
# parsed_object_code_dict_list = sic_object_code_parser(object_code_file)
#
# for line in parsed_object_code_dict_list:
#     print(line)
