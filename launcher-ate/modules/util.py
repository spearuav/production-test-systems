import traceback
import logging
from pathlib import Path
import os

# Global variables
BASE_DIR: Path = None
logger = None

def clear_terminal():
    # 'nt' מייצג את Windows, אחרת מדובר ב-Linux או macOS (posix)
    os.system('cls' if os.name == 'nt' else 'clear')

def set_base_dir(file: str):
    global BASE_DIR
    BASE_DIR = Path(file).resolve().parent

def get_base_dir() -> Path:
    """
    Returns the base directory of the project.
    """
    return BASE_DIR

def setup_logger(log_file_path: Path = None):
    """Setup the logger for debug output."""
    global logger
    
    if log_file_path is None:
        # Create a default debug log file in the base directory
        base_dir = get_base_dir()
        if base_dir is not None:
            log_file_path = base_dir / "debug.log"
        else:
            # Fallback if base dir is not set yet
            log_file_path = Path("debug.log")
    
    # Create logger
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    
    return logger

def write_exception_to_log():
    """Write exception to debug log using the standard logger."""
    if logger is not None:
        logger.exception("An exception occurred")
    else:
        # Fallback to stderr if no logger is set up
        traceback.print_exc()

