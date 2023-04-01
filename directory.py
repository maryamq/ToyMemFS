from base_file import FileType, BaseFile
from logging_utils import FileReturnCodes


class Directory(BaseFile):
    """ Represents a directory in the in memory filesystem."""

    def __init__(self, name, parent=None):
        super().__init__(name, FileType.DIR, parent)
        self._children = {}

    def __iter__(self):
        return iter(self._children.values())

    def is_empty(self):
        return len(self._children) == 0

    def has_child(self, child: str, type=None) -> bool:
        has_child = child and child in self._children
        if type:
            has_child = has_child and self._children[child].type == type
        return has_child

    def get_child(self, child: str):
        return self._children[child]

    def add_content(self, child: BaseFile, **kwargs):
        if self.has_child(child.name):
            return FileReturnCodes.ALREADY_EXIST
        self._children[child.name] = child
        child.parent = self
        return FileReturnCodes.SUCCESS

    def children_names(self):
        return self._children.keys()

    def remove_child(self, child_name, force_del=False):
        if child_name in self._children:
            child = self._children[child_name]
            if not force_del and Directory.IsDirectory(child) and len(child) > 1:
                return FileReturnCodes.INVALID_PATH
            del self._children[child_name]
            return FileReturnCodes.SUCCESS
        return FileReturnCodes.DELETE_FAILED

    def list_all(self, level=0) -> str:
        """ Helper function to output all children with indentation.
        """
        indent = ""
        indent = indent + ("\t" * level)
        all_content_names = ", ".join(self.children_names())
        return f"{indent}{self.name}: [{all_content_names}]"

    def __str__(self) -> str:
        """ Returns the list of all files in this directory.
        """
        return self.list_all(level=0)

    @classmethod
    def IsDirectory(cls, type: FileType) -> bool:
        return type == FileType.DIR


#  TODO(maryamq): Testing code. Delete it later.
if __name__ == "__main__":
    dir = Directory("/")
    dir.add_content(Directory("Hello"))
    dir.add_content(Directory("World"))
    print(dir)
    print(dir.list_all(level=5))
    print("Existing child: This should fail: ",
          dir.add_content(Directory("Hello")))
    print("Checking for children : Should exist",
          dir.has_child("Hello", FileType.DIR))
    print("Checking for child with type : Should be false",
          dir.has_child("Hello", FileType.TEXT_FILE))
    print("Absolute path: ", dir.get_child("Hello").absolute_path)
