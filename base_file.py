""" ABC for creating file objects. """

from abc import abstractmethod
from enum import Enum
from abc import ABC, abstractmethod


class FileType(Enum):
    """ Types of files supported by this filesystem. 
        TODO(maryamq): Switch to a decorator registration pattern if time. 
        This is clunky. Ideally, we should be able to add new filetypes without modifying this file. 
    """
    DIR = 0  # Directory. Contains other files.
    CONTENT_FILE = 1  # File with content.


class BaseFile(ABC):
    """ Base class for all File System objects. Everything stored in the in-mem FS should sub-class from this. """

    def __init__(self, name: str, type: FileType, parent=None):
        """ Initialize a file object.
        Argument:
        name: name of the file.
        type: type of file.
        parent: Can be another BaseFile or None.
        """
        self.name = name
        self._type = type
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def type(self) -> FileType:
        return self._type

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def absolute_path(self):
        """ Helper function to generate the absolute path."""
        # TODO(maryamq): Really should cache this (p1). We call this frequently but it is not an issue right now with a toy setup.
        path_sep = "/"
        components = []
        cur_art = self
        while cur_art:
            components.append(cur_art.name)
            cur_art = cur_art.parent
        abs_path = path_sep.join(components[::-1])
        if components[-1] == path_sep and len(components) > 1:  # edge case
            return abs_path[1:]
        return abs_path

    @abstractmethod
    def __iter__(self):
        pass
