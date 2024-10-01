import json
import importlib.resources as pkg_resources

class TafserError(Exception):
    """Custom exception class for Tafser errors."""
    pass

class Tafser:
    def __init__(self):
        self.tafsir_data = self.load_data()

    def load_data(self):
        """Helper function to load Tafsir JSON data using importlib.resources."""
        # Load tafser.json from package resources
        with pkg_resources.open_text("qurane", "tafser.json", encoding="utf-8") as file:
            return json.load(file)

    def get_tafsir(self, chapter, verse):
        """Get the tafsir for a specific verse."""
        try:
            return self.tafsir_data[str(chapter)][verse - 1]['text']
        except KeyError:
            raise TafserError(f"Tafsir for chapter {chapter} or verse {verse} not found.")
        except IndexError:
            raise TafserError(f"Tafsir for verse {verse} not found in chapter {chapter}.")
