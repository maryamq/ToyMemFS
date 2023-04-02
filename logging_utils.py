""" Kitchen sink of utility classes for logging, error messaging, etc. 
"""
from collections import namedtuple
import sys
from constants import Commands


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

    # TODO(maryamq): Create string constants for command names.
    commands = {
        Commands.LS: Command(name=Commands.LS, validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=2)], description="Lists all files in the current or specified directory.", usage="ls <enter> or ls <path>"),
        Commands.MKDIR: Command(name=Commands.MKDIR, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Creates a new directory.", usage="mkdir <path>"),
        Commands.MK: Command(name=Commands.MK, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Creates a directory or a text file. Only .txt extension in supported.", usage="mk mydir or mk myfile.txt"),
        Commands.MVFILE: Command(name=Commands.MVFILE, validators_fns=[ArgValidators.get_min_max_fn(min_value=3, max_value=3)], description="Moves a file to a new directory.", usage="mv <old_path> <new_path>"),
        Commands.FIND: Command(name=Commands.FIND, validators_fns=[ArgValidators.get_min_max_fn(min_value=3, max_value=None)], description="Search for dir or in a text file.", usage="find . regex or find <path> regex. Use ^term$ for exact match."),
        Commands.WRITE: Command(name=Commands.WRITE, validators_fns=[ArgValidators.get_min_max_fn(min_value=3, max_value=None)], description="Append or overwrite to an existing file.", usage="write <path> [-a] 'content'"),
        Commands.CAT: Command(name=Commands.CAT, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Output file content.", usage="cat <path>"),
        Commands.RM: Command(name=Commands.RM, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Removes a file or directory. Directories must be empty.", usage="rm <path>"),
        Commands.PWD: Command(name=Commands.PWD, validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=1)], description="Prints the present working directory.", usage="pwd <enter>"),
        Commands.CD: Command(name=Commands.CD, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Change present working directory.", usage="cd <dir>"),
        Commands.HELP: Command(name=Commands.HELP, validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=2)], description="Get Help.", usage="help <enter> or help <command>"),
        Commands.SYS: Command(name=Commands.SYS, validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=1)], description="Prints out all files in the drive. ", usage="sys <enter>"),
        Commands.LOAD: Command(name=Commands.LOAD, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Execute commands from file for testing", usage="load <path>"),
        Commands.NEW: Command(name=Commands.NEW, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Creates a new virtual drive", usage="new test_drive"),
        Commands.MOUNT: Command(name=Commands.MOUNT, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=2)], description="Mounts an existing virtual drive.", usage="mount test_drive"),
        Commands.DRIVES: Command(name=Commands.DRIVES, validators_fns=[ArgValidators.get_min_max_fn(min_value=1, max_value=1)], description="Lists all virtual drives.", usage="drives <enter>"),
        Commands.ECHO: Command(name=Commands.ECHO, validators_fns=[ArgValidators.get_min_max_fn(min_value=2, max_value=None)], description=Commands.ECHO, usage="echo some text"),
    }

    @classmethod
    def validate(cls, command_arr: list[str]) -> bool:
        """ Helper function to validate command. Useful for basic syntax checks.
        Argument:
        command_arr: list of command and it's arguments.
        Returns: True if the command is valid. 
        """
        cmd = command_arr[0]
        if cmd not in CommandValidator.commands:
            return False, Commands.UNKNOWN
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
    # Defaults to console. Can be changed to a file.
    log_out = sys.stdout

    # Disables the logger. Set it to True in prod.
    disable = False

    @classmethod
    def get_logger_fn(cls, src_prefix: str):
        """ Returns an function to print debugging output.
        Arguments:
        src_prefix: This string will be prefixed to all output to identify the source of the message.
        """
        prefix = f"{src_prefix}: "
        print(cls.disable)

        def log_print(*args):
            if not cls.disable and DebugLogger.log_out:
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
