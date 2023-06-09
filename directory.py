from base_file import FileType, BaseFile
from file_return_codes import FileReturnCodes
import re
from file_extension_registry import register_file_ext


@register_file_ext(ext="") # No extension = directory.
class Directory(BaseFile):
    """ Represents a directory in the in memory filesystem.
    """

    def __init__(self, name, parent=None):
        super().__init__(name, FileType.DIR, parent)
        self._children = {}

    def __iter__(self):
        return iter(self._children.values())

    def is_empty(self) -> bool:
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

    def move(self, new_parent: BaseFile):
        # A dir can only be moved to another dir.
        if not Directory.IsDirectory(new_parent.type):
            return FileReturnCodes.INVALID_PATH
        # Check if the dir already exists.
        if self.name in new_parent:
            return FileReturnCodes.ALREADY_EXIST
        self.parent.remove_child(self.name)
        new_parent.add_content(self)
        return FileReturnCodes.SUCCESS

    def delete(self) -> int:
        """ Deletes the file. """
        if self.is_empty() and self.parent:
            self.parent.remove_child(self.name)
            return FileReturnCodes.SUCCESS
        return FileReturnCodes.DELETE_FAILED

    def search(self, term, **config):
        # Todo(maryamq): Not the most efficient implementation. Fix it.
        search_term_regex = re.compile(term)
        absolute_path = self.absolute_path
        if absolute_path == "/":  # syntactic.. to avoid //
            absolute_path = ""
        results = []
        for file_name in self._children.keys():
            if len(search_term_regex.findall(file_name)) > 0:
                results.append(f"{absolute_path}/{file_name}")
        return results

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
    dir.add_content(Directory("H"))
    dir.add_content(Directory("World"))
    print(dir)
    print(dir.list_all(level=5))
    print("Existing child: This should fail: ",
          dir.add_content(Directory("Hello")))
    print("Checking for children : Should exist",
          dir.has_child("Hello", FileType.DIR))
    print("Checking for child with type : Should be false",
          dir.has_child("Hello", FileType.TEXT_FILE))
    hello_dir = dir.get_child("Hello")
    print("Absolute path: ", hello_dir.absolute_path)
    print("Search: ", dir.search("H"))
    print("Search: ", dir.search("^H$"))
    hello_dir.add_content(Directory("Inside Hello"))
    print(hello_dir.list_all())
    print(hello_dir.delete())
    print(hello_dir.list_all())
