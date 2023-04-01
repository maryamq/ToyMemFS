""" Kitchen sink of utility classes for logging, error messaging, etc. 
"""
from collections import namedtuple
import sys


class FileReturnCodes:
    """ Helper for consistent error codes and messaging. 
    This exists mostly to save keystrokes.
    """

    # Constants representing various file-related errors.
    SUCCESS = 0
    ALREADY_EXIST = 1
    CREATION_SUCCESSFUL = 2
    INVALID_PATH = 3

    # Error templates.
    _error_tmpl = {
        SUCCESS: "Success! {message} {name}",
        CREATION_SUCCESSFUL: "Creation Successful: {name}",
        ALREADY_EXIST: "Error: Already Exists: {name}",
        INVALID_PATH: "Error: Invalid path: {name} ",
    }

    @classmethod
    def print_message(cls, return_code, **kwargs) -> str:
        """ Generates an error message using the error code and kwargs.
         Arguments:
          return_code: int to represent a error code. 
          kwargs: string key-value args to populate the error template.
        """
        print(FileReturnCodes._error_tmpl[return_code].format(**kwargs).trim())


class CommandValidator:
    """
    This class performs some basic validation on commands and inputs. It checks for the min/max number of arguments supported by each command. 
    It can be extended to support more complex validation,
    """
    # Config tuple.
    Command = namedtuple("Command", [
                         'name', 'min_args', 'max_args', 'valid_arg_names', 'description', 'usage'])
    """ Simple tuple to store command meta-data for validation. This can be useful if validation becomes more complex."""
    commands = {
        "ls": Command(name="ls", min_args=0, max_args=1, description="Lists all files in the current or specified directory.", usage="ls <enter> or ls <path>", valid_arg_names=None),
        "mkdir": Command(name="mkdir", min_args=1, max_args=1, description="Creates a new directory.", usage="mkdir <path>", valid_arg_names=None),
        "pwd": Command(name="pwd", min_args=0, max_args=0, description="Prints the present working directory.", usage="pwd <enter>", valid_arg_names=None),
        "cd": Command(name="cd", min_args=1, max_args=1, description="Change present working directory.", usage="cd <dir>", valid_arg_names=None),
        "help": Command(name="help", min_args=0, max_args=1, description="Get Help.", usage="help <enter> or help <command>", valid_arg_names=None),
    }
    _UNKNOWN_COMMAND = "Unknown Command. Type help for a complete list."

    @classmethod
    def validate(cls, command_arr: list[str]) -> bool:
        """ Helper function to validate command. Useful for basic syntax checks.
        Argument:
        command_arr: list of command and it's arguments.
        Returns: True if the command is valid. 
        """
        cmd = command_arr[0]
        if cmd not in CommandValidator.commands:
            return False, CommandValidator._UNKNOWN_COMMAND
        cmd_config = CommandValidator.commands[cmd]
        # One entry is the command itself. Exclude it.
        arg_len = len(command_arr) - 1
        if arg_len < cmd_config.min_args or arg_len > cmd_config.max_args:
            return False, cmd_config.usage
        return True, ""

    @classmethod
    def help(cls, command=None) -> str:
        """ Generates help message. 
        If command is None or empty then return full help.
        """
        if command:
            if command not in CommandValidator.commands:
                return CommandValidator._UNKNOWN_COMMAND
            return cls._help_message(CommandValidator.commands[command])
        all_cmd = [CommandValidator._help_message(
            cfg) for cfg in CommandValidator.commands.values()]
        return "\n".join(all_cmd)

    @classmethod
    def _help_message(cls, cmd_config):
        """
        Helper method to format the message
        """
        return f"{cmd_config.name}: {cmd_config.description} Usage: {cmd_config.usage}"


class DebugLogger:
    """ 
    A utility class for logging and debugging. 
    """
    # Routes debugging output to this file. Defaults to console. Can be changed to a file.
    #
    # Defaults to console. Can be changed to a file or disabled entirely by setting this to None.
    log_out = sys.stdout

    @classmethod
    def get_logger_fn(cls, src_prefix: str):
        """ Returns an function to print debugging output.
        Arguments:
        src_prefix: This string will be prefixed to all output to identify the source of the message.
        """
        def log_print(*args):
            if DebugLogger.log_out:
                print(*args, file=DebugLogger.log_out)
        return log_print


# TODO(maryamq): Testing.. to be deleted.
if __name__ == "__main__":
    print(CommandValidator.validate("ls blah blah".split()))
    print(CommandValidator.validate("mkdir blah".split()))
    print(CommandValidator.validate("help mkdir".split()))
    print(CommandValidator.help())
    print(CommandValidator.help("ls"))
    log = DebugLogger.get_logger_fn("test")
    log("Logging")
