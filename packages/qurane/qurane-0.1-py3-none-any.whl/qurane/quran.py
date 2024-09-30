# quran.py

import json
import os

class QuranError(Exception):
    """Custom exception class for Quran library errors."""
    pass

class Quran:
    def __init__(self, quran_file="quran.json"):
        self.quran_data = self.load_data(quran_file)

    def load_data(self, file_path):
        """Helper function to load JSON data."""
        if not os.path.exists(file_path):
            raise QuranError(f"File {file_path} not found.")
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_verse(self, chapter, verse):
        """Get a specific verse by chapter and verse number."""
        try:
            return self.quran_data[str(chapter)][verse - 1]['text']
        except KeyError:
            raise QuranError(f"Chapter {chapter} or verse {verse} not found.")
        except IndexError:
            raise QuranError(f"Verse {verse} not found in chapter {chapter}.")
            