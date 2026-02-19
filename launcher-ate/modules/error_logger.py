


from enum import IntEnum, auto
from logo_reader import LogoReader
from util import BASE_DIR
from colorama import Fore, Back, Style


class Error_types(IntEnum):
    FILE = auto()
    LOGO = auto()
    TESTS = auto()
class Error_severity(IntEnum):
    WARN = auto()
    ERROR = auto()

LOGO_FULL_PATH = BASE_DIR/'logo'

ERROR_HANDLING_DICT:dict[Error_types,dict[type,str]] = {
    Error_types.LOGO : {
        FileNotFoundError: f"The logo file: {LogoReader.get_filename()} wasn't found in {BASE_DIR}",
        PermissionError: f"Bad file permission for {LOGO_FULL_PATH}",
        IsADirectoryError: f"{LOGO_FULL_PATH} is a folder (should be a file)",
        UnicodeDecodeError: f"The file {LOGO_FULL_PATH} contains invalid characters",
        Exception: f"Unexpected error reading {LOGO_FULL_PATH}"
    },
    None: {Exception: "Unexpected error: {message}"}
}

def error_formater(e:Exception, type_:type, severity:Error_severity):
    if severity is None: severity=Error_severity.ERROR
    severity_message_dict: dict[Error_severity,str] = {
        Error_severity.ERROR: "ERROR:",
        Error_severity.WARN: "Warning:"
    }
    severity_color_dict: dict[Error_severity,str] = {
        Error_severity.ERROR: Fore.RED,
        Error_severity.WARN: Fore.YELLOW
    }

    not_found = {} # uniqu reference and safe dict

    # search for  type->error, none->error, type->Exception, none->Exception
    message = ERROR_HANDLING_DICT.get(type_,not_found).get(type(e),not_found)
    if message is not_found:
        message = ERROR_HANDLING_DICT.get(None,not_found).get(type(e),not_found)
    if message is not_found:
        message = ERROR_HANDLING_DICT.get(type_,not_found).get(Exception,not_found)
    if message is not_found:
        message = ERROR_HANDLING_DICT.get(None).get(Exception) # hardcoded can't fail
    return f"{severity_color_dict(severity)}{severity_message_dict(severity)}{Style.RESET_ALL}{message}"