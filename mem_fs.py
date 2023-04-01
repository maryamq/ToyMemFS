from io import StringIO
from base_file import BaseFile, FileType
from virtual_mem_drive_registry import VirtualMemDriveRegistry
from directory import Directory
from logging_utils import FileReturnCodes, DebugLogger
import path_utils


class MemFileSystem(metaclass=VirtualMemDriveRegistry):
    ROOT_DIR = "/"

    def __init__(self, name):
        self._name = name
        self._root = Directory(MemFileSystem.ROOT_DIR)
        self._children = {}
        self._logger = DebugLogger.get_logger_fn("MemFileSystem_" + name)

    @property
    def root(self):
        return self._root

    @property
    def name(self):
        return self._name

    def get_dir(self, working_dir: Directory, input_path: str) -> tuple[Directory, FileReturnCodes]:
        base_dir, unmatched = self.get_valid_dir(working_dir, input_path)
        if unmatched:
            return None, FileReturnCodes.INVALID_PATH
        return base_dir, FileReturnCodes.SUCCESS

    def get_valid_dir(self, working_dir: Directory, input_path: str):
        """ This function encapsulate all the complexities of resolving base directory.
        It takes pwd into account. 
        e.g get_base_dir(pwd, "/hello/world) -> disregard pwd and return /hello dir.
        get_base_dir(pwd, "myfile")-> returns present working dir.
        get_base_dir(pwd, "...")-> Returns parent dir
        """
        working_dir_path = working_dir.absolute_path
        path_parts = path_utils.merge_and_deconstruct(
            working_dir_path, input_path)
        cur_dir = self.root
        parts_idx = 1
        # Recurse through the tree.
        while parts_idx < len(path_parts):
            if cur_dir.has_child(path_parts[parts_idx], FileType.DIR):
                cur_dir = cur_dir.get_child(path_parts[parts_idx])
                parts_idx += 1
            else:
                break
        return cur_dir, path_parts[parts_idx:]

    def make_dir(self, working_dir: Directory, new_dir_path: str) -> FileReturnCodes:
        valid_base_dir, unmatched_dir = self.get_valid_dir(
            working_dir, new_dir_path)
        if len(unmatched_dir) != 1 or not unmatched_dir[0]:
            return FileReturnCodes.INVALID_PATH
        dir_name = unmatched_dir[0]
        self._logger(
            f"Attempting to create dir {dir_name} in {valid_base_dir.absolute_path}")
        return valid_base_dir.add_new_child(Directory(dir_name))

    def list_all(self, base_dir: Directory, file_path=None):
        if file_path:
            raise NotImplementedError()
        return base_dir.list_all()

    def __str__(self) -> str:
        """ Retruns a string representation of the file system. 
        Useful for debugging/logging.
        """
        queue = []
        queue.append((self._root, 0))
        level = 0
        output = StringIO()
        # Basic bfs
        while queue:
            directory, level = queue.pop(0)
            output.write(directory.list_all(level=level))
            output.write("\n")
            for item in directory:
                if item.type == FileType.DIR:
                    queue.append((item, level+1))
        final_str = output.getvalue()
        output.close()  # free up buffer
        return final_str


if __name__ == "__main__":
    fs = MemFileSystem("test")
    print(fs.make_dir(fs.root, "hello"))
    print(fs.make_dir(fs.root, "movie"))
    print(fs.make_dir(fs.root, "tv"))
    print(fs.list_all(fs.root))
    print(fs.make_dir(fs.root, "/movie/disney"))
    print(fs.make_dir(fs.root, "/movie/paramount"))
    print(fs.get_dir(fs.root, "/movie/disney"))
    print(fs)
