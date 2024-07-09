import logging
import json


class File:
    def __init__(self, path_to_file):
        self.logger = logging.getLogger("file-class")

        self.path_to_file = path_to_file
        try:
            open(self.path_to_file)
        except FileNotFoundError as file_not_found_exception:
            self.logger.critical(f"Invalid path to file : {self.path_to_file}")
            raise file_not_found_exception

    def read_data(self):
        with open(self.path_to_file, 'r') as file:
            return json.load(file)

    def write_data(self, data):
        with open(self.path_to_file, 'w') as file:
            file.write(json.dumps(data))
