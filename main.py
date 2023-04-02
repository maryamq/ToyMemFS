import virtual_mem_drive_registry
from mem_fs import MemFileSystem, FileType
from environment import Environment
from logging_utils import CommandValidator
from file_return_codes import FileReturnCodes
import os
from constants import Commands

# Helper function to check if cmd line arguments are provided.
def has_cmd_arg(command_line_arr: list[str]) -> bool:
    return len(command_line_arr) > 1 and command_line_arr[1]


def execute_commands_from_file(file_name):
    """ Reads and executes commands from a file. Useful for testing.
    Once the commands are executed, the control is passed back to the user.
    """
    all_commands = ""
    with open(file_name) as f:
        all_commands = f.readlines()
    for line in all_commands:
        comps = line.strip().lower().split(" ")
        if not comps:
            continue
        valid_cmd_syntax, msg = CommandValidator.validate(comps)
        if not valid_cmd_syntax:
            print(f"Error executing line: {line}. {msg}")
        else:
            process_command(comps)
    print(
        f"Executed {len(all_commands)} commands. Type sys <enter> to view the structure. Starting user IO\n\n")


def execute_commands_from_io():
    """ This function handles user's input."""
    while True:
        try:
            line = input(env.prompt).strip().lower()
            if not line or line ==  Commands.EXIT:
                print("GoodBye!")
                return
            comps = line.split(" ")

            # Catch Errors early.
            valid_cmd_syntax, msg = CommandValidator.validate(comps)
            if not valid_cmd_syntax:
                print(comps)
                print(f"Invalid Command: {msg}")
                continue
            process_command(comps)
        except Exception as e:  # catching all exception here to avoid destroying state.
            print(e)


def process_command(comps):
    command = comps[0]
    if command == Commands.LS:
        if has_cmd_arg(comps):
            dir_path = comps[1]
            dir_obj, ret = env.current_drive.get_dir(
                env.present_working_dir, dir_path)
            FileReturnCodes.print_message(
                ret, message="Listing files in: ", name=comps[1])
            if ret == FileReturnCodes.SUCCESS:
                print(dir_obj)
        else:
            print(env.present_working_dir)
    elif command == Commands.PWD:
        print(env.present_working_dir.absolute_path)
    elif command == Commands.CD:
        valid_dir, ret = env.current_drive.get_dir(
            env.present_working_dir, comps[1])
        if ret == FileReturnCodes.SUCCESS:
            env.present_working_dir = valid_dir
        FileReturnCodes.print_message(ret, name=comps[1])
    elif command == Commands.MK:
        ret = env.current_drive.make_file(
            env.present_working_dir, comps[1], FileType.DIR)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Created ", err_msg="Problem with your file extension:")
    elif command == Commands.RM:
        dir_obj, ret = env.current_drive.get_file(
            env.present_working_dir, comps[1])
        if ret == FileReturnCodes.SUCCESS:
            dir_obj.delete()
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Deleted ")
    elif command == Commands.MK:
        ret = env.current_drive.make_file(
            env.present_working_dir, comps[1], FileType.TEXT_FILE)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Created ")
    elif command == Commands.MVFILE:
        selected_file, future_dir = comps[1], comps[2]
        ret = env.current_drive.move_file(
            env.present_working_dir, selected_file, future_dir)
        FileReturnCodes.print_message(ret, name=comps[1], success_msg="Moved ")
    elif command == Commands.WRITE:
        path = comps[1]
        mode = "overwrite"
        content_idx = 2
        if len(comps) > 3 and comps[2] in ["-a"]:
            mode = "append"
            content_idx += 1
        content = " ".join(comps[content_idx:])
        file, ret = env.current_drive.get_file(
            env.present_working_dir, path, type=FileType.TEXT_FILE)
        if ret == FileReturnCodes.SUCCESS:
            file.add_content(content, write_mode=mode)
        FileReturnCodes.print_message(ret, name=comps[1])
    elif command == Commands.CAT:
        file, ret = env.current_drive.get_file(
            env.present_working_dir, comps[1], type=FileType.TEXT_FILE)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Content For ")
        if ret == FileReturnCodes.SUCCESS:
            print(file)
    elif command == Commands.FIND:
        file_to_search = comps[1]
        search_term = " ".join(comps[2:])
        print("Searching for terms: ", search_term)
        search_results, ret = env.current_drive.search(
            env.present_working_dir, file_to_search, search_term)
        if ret == FileReturnCodes.SUCCESS:
            print(f"Found {len(search_results)} entries")
            print(search_results)
        else:
            FileReturnCodes.print_message(ret, name=comps[1])
    # ****************Commands for Managing a new FS.************n
    elif command == Commands.NEW:
        if not has_cmd_arg(comps):
            print("Missing drive name. Usage: new <drive_name>")
            return
        new_drive_name = comps[1]
        if comps[1] in virtual_mem_drive_registry.registry:
            print(
                f"Error: {comps[1]} already exists. Please specify a new name.")
            return
        fs = MemFileSystem(comps[1])
        print(f"Creating a new in-memory drive: {fs.name}")
    elif command == Commands.DRIVES:
        print("List of all drives")
        for k in virtual_mem_drive_registry.registry.keys():
            print(k)
    elif command == Commands.MOUNT:
        if not has_cmd_arg(comps) or comps[1] not in virtual_mem_drive_registry.registry:
            print("Error! Please specify an existing drive name.")
            return
        current_drive = virtual_mem_drive_registry.registry[comps[1]]
        env.current_drive = current_drive
        print("Switched Drives: ", env.current_drive.name)
    elif command == Commands.LOAD:
        print("Loading file: ", comps[1])
        execute_commands_from_file(comps[1])
    elif command == Commands.ECHO:
        print(" ".join(comps[1:]))
    elif command == Commands.SYS:
        print(env.current_drive)
    elif command == Commands.HELP:
        cmd_name = comps[1] if len(comps) > 1 else None
        print(CommandValidator.help(cmd_name))
    else:
        print("Unknown Command!")


if __name__ == "__main__":
    env = Environment.get_default()
    print("Welcome to InMemFS. Type help to get started. Press Enter to exit.")
    execute_commands_from_io()
