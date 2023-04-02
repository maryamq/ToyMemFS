""" Classes for supporting content files include text.
"""

from io import StringIO
from base_file import FileType, BaseFile
from directory import Directory
from file_return_codes import FileReturnCodes


class TextFile(BaseFile):
    """ Supports plain text files.
    """

    # Config args supported by this type.
    _default_config = {
        "write_mode": "overwrite" # supported: overwrite | append
    }

    def __init__(self, name: str, parent: Directory):
        """ Initialize a text file.
        Arguments:
        name: name of the file.
        parent: Directory that holds this file.
        """
        super().__init__(name, FileType.TEXT_FILE, parent)
        self._content = StringIO()

    def __iter__(self):
        self._content.flush()
        return iter(self._content)

    def is_empty(self):
        return len(self._content) == 0

    def add_content(self, content, **kwargs):
        """ Adds text content to the file. We either append or overwrite.
        """
        config = TextFile._default_config
        if kwargs:
            config.update(kwargs)
        if config["write_mode"] == "append":
            self._content.writelines(content)
        else:
            # overwrite
            self._content.truncate(0)
            self._content.writelines(content)
    
    def move(self, new_parent:Directory):
        if self.name in new_parent:
            return FileReturnCodes.ALREADY_EXIST
        self.parent.remove_child(self.name)
        new_parent.add_content(self)
        return FileReturnCodes.SUCCESS

    def __str__(self)->str:
        return self._content.getvalue()

    def delete(self) -> int:
        self._content.close()
        super().delete()
