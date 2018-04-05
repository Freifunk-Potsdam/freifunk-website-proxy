"""
A simple way to save and store the data of the server.

"""
import pickle
import os


class Database:
    """Save and store data in a file"""
    
    def __init__(self, file):
        """Create a new database which saves and loads objects from a file."""
        self.file = file
    
    def save(self, obj):
        """Save an object to the file."""
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "wb") as f:
            pickle.dump(obj, f)
    
    def load(self):
        """Load an object from the file."""
        if not os.path.isfile(self.file):
            return None
        with open(self.file, "rb") as f:
            return pickle.load(f)
    
    def load_save(self):
        """Load the object from the file but return None in case of an error."""
        try:
            return self.load()
        except:
            import traceback
            traceback.print_exc()
            return None


class NullDatabase:
    """This is a database which can not store anything."""
    
    def save(self, obj):
        """Do not save the object."""
    
    def load(self):
        """Load nothing."""
        return None
    load_safe = load


__all__ = ["Database"]

