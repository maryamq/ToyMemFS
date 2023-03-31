from directory import Directory
from mem_fs import MemFileSystem


class Environment:
    """ A helper class to manage user state such as present working dir, current drive etc.
        Any user-related config objects (such as permission objects) should be kept here.
    """
    _DEFAULT_PROMPT = ">"

    def __init__(self):
        """ Initializes user's environment."""
        self._current_drive = None
        # TODO(maryamq): maybe this should belong to individual in-mem drive.
        self._pwd = None

    @classmethod
    def get_default(cls):
        """Creates a default environment."""
        env = Environment()
        env.current_drive = MemFileSystem("Default")
        return env

    @property
    def current_drive(self):
        """ Returns the current drive. A user can have mulitple drives.
        """
        return self._current_drive

    @current_drive.setter
    def current_drive(self, drive: MemFileSystem):
        """ Sets the current drive."""
        self._current_drive = drive
        self._pwd = self._current_drive.root

    @property
    def present_working_dir(self):
        """ Returns the present working dir. 
        """
        return self._pwd

    @present_working_dir.setter
    def present_working_dir(self, pwd: Directory):
        """ Sets the pwd. (similar to cd <path>)"""
        self._pwd = pwd

    @property
    def prompt(self):
        """ Shows prompt at Input() for useability."""
        if not self._current_drive:
            return Environment._DEFAULT_PROMPT
        return f"{self._current_drive.name}>"

