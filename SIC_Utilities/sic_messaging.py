# Constants
TEXT_COLOR_RED = "\033[91m"
TEXT_COLOR_GREEN = "\033[92m"
TEXT_COLOR_DEFAULT = "\033[0m"


def print_status(text_line_1, text_line_2=None):
    status_message = text_line_1

    if text_line_2 is not None:
        status_message = status_message + "\n" + text_line_2

    print(TEXT_COLOR_GREEN + status_message + TEXT_COLOR_DEFAULT)


def print_error(text_line_1, text_line_2=None):
    error_message = text_line_1

    if text_line_2 is not None:
        error_message = error_message + "\n" + text_line_2

    print(TEXT_COLOR_RED + error_message + TEXT_COLOR_DEFAULT)
