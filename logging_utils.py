""" Kitchen sink of utility classes for logging, error messaging, etc. 
"""
from collections import namedtuple
import sys


class ArgValidators:
    """ Utility class for validating arguments. 
    This can be extended to support additional validations.
    """
    @classmethod
    def get_min_max_fn(cls, *, min_value=None, max_value=None):
        """ Returns true if number of arguments are within min/max range.
        """
        def min_max_fn(command_arr: list[str]) -> bool:
            arg_len = len(command_arr)
            return (not min_value or arg_len >= min_value) and (not max_value or arg_len <= max_value)
        return min_max_fn


class CommandValidator:
    """
    This class performs some basic validation on commands and inputs. It checks for the min/max number of arguments supported by each command. 
    It can be extended to support more complex validation,
    """
    # Config tuple.
    """ Simple tuple to store command meta-data for validation. This can be useful if validation becomes more complex.
        name: Name of the command
        validators_fn: Array of validation functions. If any of these fns are False, then the command syntax is invalid.
        description: Description of the command.
        usage: A short description on how to use the command.
        """
    Command = namedtuple("Command", [
                         'name', 'validators_fns', 'description', 'usage'])

    commands = {
        "ls": Command(name="ls", validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=2)], description="Lists all files in the current or specified directory.", usage="ls <enter> or ls <path>"),
        "mkdir": Command(name="mkdir", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Creates a new directory.", usage="mkdir <path>"),
        "mkfile": Command(name="mkfile", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Creates a text file.", usage="mkfile <path>"),
        "mvfile": Command(name="mvfile", validators_fns=[ArgValidators.get_min_max_fn(min_value=3, max_value=3)], description="Moves a file to a new directory.", usage="mv <old_path> <new_path>"),
        "write": Command(name="write", validators_fns=[ArgValidators.get_min_max_fn(min_value=3, max_value=None)], description="Append or overwrite to an existing file.", usage="write <path> [-a] 'content'"),
        "cat": Command(name="cat", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Output file content.", usage="cat <path>"),
        "rm": Command(name="rm", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Removes a file or directory. Directories must be empty.", usage="rm <path>"),
        "pwd": Command(name="pwd", validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=1)], description="Prints the present working directory.", usage="pwd <enter>"),
        "cd": Command(name="cd", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Change present working directory.", usage="cd <dir>"),
        "help": Command(name="help", validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=2)], description="Get Help.", usage="help <enter> or help <command>"),
        "sys": Command(name="sys", validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=1)], description="Prints out all files in the drive. ", usage="sys <enter>"),
        "load": Command(name="load", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Execute commands from file for testing", usage="load <path>"),
        "echo": Command(name="echo", validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=None)], description="echo", usage="echo some text"),

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
        # Iterate through validators.
        for valid_fn in cmd_config.validators_fns:
            if not valid_fn(command_arr):
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
        prefix = f"{src_prefix}: "

        def log_print(*args):
            if DebugLogger.log_out:
                print(prefix, *args, file=DebugLogger.log_out)
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
