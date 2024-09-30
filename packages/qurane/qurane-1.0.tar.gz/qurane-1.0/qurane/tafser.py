# tafser.py

import json
import os

class TafserError(Exception):
    """Custom exception class for Tafser errors."""
    pass

class Tafser:
    def __init__(self, tafsir_file="tafser.json"):
        self.tafsir_data = self.load_data(tafsir_file)

    def load_data(self, file_path):
        """Helper function to load JSON data."""
        if not os.path.exists(file_path):
            raise TafserError(f"File {file_path} not found.")
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_tafsir(self, chapter, verse):
        """Get the tafsir for a specific verse."""
        try:
            return self.tafsir_data[str(chapter)][verse - 1]['text']
        except KeyError:
            raise TafserError(f"Tafsir for chapter {chapter} or verse {verse} not found.")
        except IndexError:
            raise TafserError(f"Tafsir for verse {verse} not found in chapter {chapter}.")
            