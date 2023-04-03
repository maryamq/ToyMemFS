"""
Methods for registring file extensions. 
Suclasses of BaseFile can register themselves as handlers of particular extensions. 
This allows the FS to scale support for new types dynamically without requiring any other code changes. 
"""
from logging_utils import DebugLogger
from file_return_codes import FileReturnCodes
from base_file import BaseFile

_extension_registry = {}
_logger = DebugLogger.get_logger_fn("ExtRegistry")


def register_file_ext(ext: str):
    """ Registers BaseFile subclass as an handler for extension.
    """
    def reg_fn(class_initializer):
        if ext in _extension_registry:
            _logger(f"Warning: Overwriting {ext} with {class_initializer}")
        assert issubclass(type(class_initializer), type(BaseFile))
        _extension_registry[ext] = class_initializer
        _logger(f"Successfully Registered {class_initializer}")
        return class_initializer
    return reg_fn


def file_creator_factory(filename, parent, *args, **kwargs):
    """
    Initializes a BaseFile subclasses based on the extension. 
    """
    # TODO(maryamq): hacky
    comps = filename.split(".")
    ext = ""
    if len(comps) > 1:
        ext = comps[-1]
    if ext not in _extension_registry:
        _logger(f"Unsupported extension: ", ext)
        return None, FileReturnCodes.UNSUPPORTED
    return _extension_registry[ext](filename, parent, *args, **kwargs), FileReturnCodes.SUCCESS
