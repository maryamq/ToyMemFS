""" Content Files for In-MEM filesystem."""
from io import StringIO
from base_file import FileType, BaseFile
from directory import Directory
from file_return_codes import FileReturnCodes
from file_extension_registry import register_file_ext
import re


@register_file_ext(ext="txt")
class TextFile(BaseFile):
    """ Supports plain text files with txt extension.
    """

    # Config args supported by this type.
    _default_config = {
        "write_mode": "overwrite"  # supported: overwrite | append
    }

    def __init__(self, name: str, parent: Directory):
        """ Initialize a text file.
        Arguments:
        name: name of the file.
        parent: Directory that holds this file.
        """
        super().__init__(name, FileType.TEXT_FILE, parent)
        self._content = StringIO()  # For supporting efficient appends.

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
        if config["write_mode"] != "append":
            self._content.truncate(0) #overwrite.
        self._content.writelines([content, "\n"])

    def move(self, new_parent: Directory):
        if self.name in new_parent:
            return FileReturnCodes.ALREADY_EXIST
        self.parent.remove_child(self.name)
        new_parent.add_content(self)
        return FileReturnCodes.SUCCESS

    def search(self, regex_str, **kwargs):
        matcher = re.compile(regex_str)
        return matcher.findall(self._content.getvalue())

    def __str__(self) -> str:
        return self._content.getvalue()

    def delete(self) -> int:
        self._content.close()
        if self.parent:
            self.parent.remove_child(self.name)
        return FileReturnCodes.SUCCESS


# TODO(maryamq): Testing. delete later.
if __name__ == "__main__":
    test_file = TextFile("test", parent=None)
    test_file.add_content("Hello World")
    print(test_file)
    print("Searching: ", test_file.search("World"))
