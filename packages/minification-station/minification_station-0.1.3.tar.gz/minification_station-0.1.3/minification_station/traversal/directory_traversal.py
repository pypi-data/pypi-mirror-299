import logging
import os

from minification_station.config.constants import (
    DEFAULT_LANGUAGE,
    LANGUAGE_CONSTANTS,
)
from minification_station.logging.decorators import log_exceptions, log_function_call


class DirectoryTraversal:
    def __init__(
        self,
        directory: str,
        program_lang: str = DEFAULT_LANGUAGE,
    ) -> None:
        constants = LANGUAGE_CONSTANTS.get(program_lang, LANGUAGE_CONSTANTS[DEFAULT_LANGUAGE])
        self.directory: str = directory
        self.file_extension: str = constants["file_extension"]
        self.ignore_files: list[str] = constants["ignore_files"]
        self.ignore_folders: list[str] = constants["ignore_folders"]
        self.file_size_limit: int = constants["file_size_limit"]

    @log_exceptions
    @log_function_call
    def get_files(self) -> list[str]:
        file_paths = []
        for root, dirs, files in os.walk(self.directory):
            # Ignore specified folders
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            for file in files:
                if file in self.ignore_files:
                    continue
                if not file.endswith(self.file_extension):
                    continue
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > self.file_size_limit:
                    continue
                file_paths.append(file_path)
        logging.info(f"Found {len(file_paths)} files")
        return file_paths
