import os
import pathlib


class LogoReader():
    base_dir = None
    FILE_NAME = "logo.ascii_art.txt"
    def __init__(self,base_dir:pathlib.Path):
        self.base_dir = base_dir
    def read(self):
        with open(self.base_dir/self.FILE_NAME) as file:
            value = file.read()
            return value
    @staticmethod
    def get_filename():
        return LogoReader.FILE_NAME
