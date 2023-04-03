from io import StringIO
from base_file import BaseFile, FileType
from virtual_mem_drive_registry import VirtualMemDriveRegistry
from directory import Directory
from content_files import TextFile
from logging_utils import DebugLogger
from file_return_codes import FileReturnCodes
import path_utils
from file_extension_registry import file_creator_factory

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

    def move_file(self, working_dir: Directory, current_path: str, future_dir_path: str) -> int:
        """ Moves a file (text or dir) to a new directory.
        Files names at the new location must be unique.
        """
        selected_file, ret_selected = self.get_file(working_dir, current_path)
        if ret_selected != FileReturnCodes.SUCCESS:
            return ret_selected
        
        # Cannot move root.
        if selected_file == self.root:
            return FileReturnCodes.UNSUPPORTED

        future_dir, ret_future_dir = self.get_dir(working_dir, future_dir_path)
        if ret_selected != FileReturnCodes.SUCCESS:
            return ret_future_dir
        return selected_file.move(future_dir)

    def get_dir(self, working_dir: Directory, input_path: str) -> tuple[Directory, int]:
        base_dir, unmatched = self.get_valid_dir(working_dir, input_path)
        if unmatched:
            return None, FileReturnCodes.INVALID_PATH
        return base_dir, FileReturnCodes.SUCCESS

    def get_file(self, working_dir: Directory, input_path: str, type=FileType.UNKNOWN) -> tuple[BaseFile, int]:
        self._logger("Getting File: ", input_path)
        base_dir, unmatched = self.get_valid_dir(working_dir, input_path)
        self._logger("base_dir, unmatched: ", base_dir, unmatched)
        if base_dir and len(unmatched) < 2:
            if not unmatched:
                # Delete the file directly.
                return base_dir, FileReturnCodes.SUCCESS
            elif base_dir.has_child(unmatched[0]):
                selected_file = base_dir.get_child(unmatched[0])
                if type == FileType.UNKNOWN or selected_file.type == type:
                    return selected_file, FileReturnCodes.SUCCESS
        return None, FileReturnCodes.INVALID_PATH

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

    def make_file(self, working_dir: Directory, new_dir_path: str, file_type: int) -> FileReturnCodes:
        valid_base_dir, unmatched_dir = self.get_valid_dir(
            working_dir, new_dir_path)
        if len(unmatched_dir) != 1 or not unmatched_dir[0]:
            return FileReturnCodes.INVALID_PATH
        file_name = unmatched_dir[0]
        self._logger(
            f"Attempting to create file '{file_name}' in {valid_base_dir.absolute_path}")
        new_file, ret = file_creator_factory(file_name, parent=valid_base_dir)
        if ret == FileReturnCodes.SUCCESS:
            return valid_base_dir.add_content(new_file)
        return ret

    def search(self, working_dir: Directory, file_path, regex):
        if not file_path or file_path == ".":
            selected_file = working_dir
        else:
            selected_file, ret_selected = self.get_file(working_dir, file_path)
            if ret_selected != FileReturnCodes.SUCCESS:
                return [], ret_selected

        if selected_file.type != FileType.DIR:
            return selected_file.search(regex), FileReturnCodes.SUCCESS
        # Handle Dir search.
        self._logger("Starting dir search : ", selected_file)
        dir_matches = []
        def action_fn(dir, _): return dir_matches.extend(dir.search(regex))
        self.recurse_dir(selected_file, action_fn)
        return dir_matches, FileReturnCodes.SUCCESS

    def list_all(self, base_dir: Directory, file_path=None):
        if file_path:
            raise NotImplementedError()
        return base_dir.list_all()

    def recurse_dir(self, start_dir, action_fn):
        queue = []
        queue.append((start_dir, 0))
        level = 0
        # Basic bfs
        while queue:
            directory, level = queue.pop(0)
            action_fn(directory, level)
            for item in directory:
                if item.type == FileType.DIR:
                    queue.append((item, level+1))

    def __str__(self) -> str:
        """ Retruns a string representation of the file system. 
        Useful for debugging/logging.
        """
        output = StringIO()

        def action_fn(dir, level): return output.write(
            f"{dir.list_all(level=level)}\n")
        self._logger("Action fn", action_fn(self._root, 0))
        self.recurse_dir(self._root, action_fn)
        final_str = output.getvalue()
        output.close()  # free up buffer
        return final_str


if __name__ == "__main__":
    fs = MemFileSystem("test")
    print(fs.make_file(fs.root, "hello", FileType.DIR))
    print(fs.make_file(fs.root, "movie",  FileType.DIR))
    print(fs.list_all(fs.root))
    print(fs.make_file(fs.root, "/movie/disney",  FileType.DIR))
    print(fs.make_file(fs.root, "hello",  FileType.DIR))
    print(fs.make_file(fs.root, "/movie/paramount",  FileType.DIR))
    print(fs.get_dir(fs.root, "/movie/disney"))
    # file writing test:
    print(fs.make_file(fs.root, "hello.txt", FileType.TEXT_FILE))
    text_file, err_code = fs.get_file(fs.root, "hello.txt", FileType.TEXT_FILE)
    print(text_file, err_code)
    text_file.add_content("hello world")
    print(text_file)
    print("Before moves")
    print(fs)
    print(fs.move_file(fs.root, "hello.txt", "/movie/disney"))
    print(fs.move_file(fs.root, "/movie/disney", "/movie/paramount"))
    print(fs)
    print("Search: ", fs.search(fs.root, "/", "dis"))
    print(fs.make_file(fs.root, "hello.sj",  FileType.DIR))
