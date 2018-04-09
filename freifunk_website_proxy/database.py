"""
A simple way to save and store the data of the server.

"""
import pickle
import os


class Database:
    """Save and store data in a file"""
    
    def __init__(self, file, version=1):
        """Create a new database which saves and loads objects from a file.
        
        - version is the version number of the database.
          Only entries of this specific version can be loaded.
        
        """
        self.file = file
        self.version = version
        
    def _make_entry(self, value):
        """Create a database entry to store."""
        return (self.version, value)
    
    def _read_entry(self, entry):
        """Get the information from the entry."""
        if entry[0] == self.version:
            return entry[1]
        return None
    
    def save(self, obj):
        """Save an object to the file."""
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "wb") as f:
            pickle.dump(self._make_entry(obj), f)
    
    def load(self):
        """Load an object from the file."""
        if not os.path.isfile(self.file):
            return None
        with open(self.file, "rb") as f:
            return self._read_entry(pickle.load(f))
    
    def load_safely(self):
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
    load_safely = load


__all__ = ["Database"]

