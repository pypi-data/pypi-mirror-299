import json
import importlib.resources as pkg_resources

class QuranError(Exception):
    """Custom exception class for Quran library errors."""
    pass

class Quran:
    def __init__(self):
        self.quran_data = self.load_data()

    def load_data(self):
        """Helper function to load JSON data using importlib.resources."""
        # Load quran.json from package resources
        with pkg_resources.open_text("quranu", "quran.json", encoding="utf-8") as file:
            return json.load(file)

    def get_verse(self, chapter, verse):
        """Get a specific verse by chapter and verse number."""
        try:
            return self.quran_data[str(chapter)][verse - 1]['text']
        except KeyError:
            raise QuranError(f"Chapter {chapter} or verse {verse} not found.")
        except IndexError:
            raise QuranError(f"Verse {verse} not found in chapter {chapter}.")
