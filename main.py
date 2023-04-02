import virtual_mem_drive_registry
from mem_fs import MemFileSystem, FileType
from environment import Environment
from logging_utils import CommandValidator
from file_return_codes import FileReturnCodes


def exit():
    print("GoodBye!")

# Helper function to check if cmd line arguments are provided.


def has_cmd_arg(command_line_arr: list[str]) -> bool:
    return len(command_line_arr) > 1 and command_line_arr[1]


def process_command(comps):
    command = comps[0]
    if command == "ls":
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
    elif command == "pwd":
        print(env.present_working_dir.absolute_path)
    elif command == "cd":
        valid_dir, ret = env.current_drive.get_dir(
            env.present_working_dir, comps[1])
        if ret == FileReturnCodes.SUCCESS:
            env.present_working_dir = valid_dir
        FileReturnCodes.print_message(ret, name=comps[1])
    elif command == "mkdir":
        ret = env.current_drive.make_file(
            env.present_working_dir, comps[1], FileType.DIR)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Created ")
    elif command == "rm":
        dir_obj, ret = env.current_drive.get_file(
            env.present_working_dir, comps[1])
        if ret == FileReturnCodes.SUCCESS:
            dir_obj.delete()
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Deleted ")
    elif command == "mkfile":
        ret = env.current_drive.make_file(
            env.present_working_dir, comps[1], FileType.TEXT_FILE)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Created ")
    elif command == "mvfile":
        selected_file, future_dir = comps[1], comps[2]
        ret = env.current_drive.move_file(
            env.present_working_dir, selected_file, future_dir)
        FileReturnCodes.print_message(ret, name=comps[1], success_msg="Moved ")
    elif command == "write":
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
    elif command == "cat":
        file, ret = env.current_drive.get_file(
            env.present_working_dir, comps[1], type=FileType.TEXT_FILE)
        FileReturnCodes.print_message(
            ret, name=comps[1], success_msg="Content For ")
        if ret == FileReturnCodes.SUCCESS:
            print(file)

    # ****************Commands for Managing a new FS.************n
    elif command == "new":
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
    elif command == "drives":
        print("List of all drives")
        for k in virtual_mem_drive_registry.registry.keys():
            print(k)
    elif command == "load":
        if not has_cmd_arg(comps) or comps[1] not in virtual_mem_drive_registry.registry:
            print("Error! Please specify an existing drive name.")
            return
        current_drive = virtual_mem_drive_registry.registry[comps[1]]
        env.current_drive = current_drive
        print("Switched Drives: ", env.current_drive.name)
    elif command == "sys":
        print(env.current_drive)
    elif command == "help":
        cmd_name = comps[1] if len(comps) > 1 else None
        print(CommandValidator.help(cmd_name))
    else:
        print("Unknown Command!")


if __name__ == "__main__":
    env = Environment.get_default()
    print("Welcome to InMemFS. Type help to get started. Press Enter to exit.")
    while True:
        try:
            line = input(env.prompt)
            if not line:
                exit()
                break
            comps = line.strip().lower().split(" ")

            # Catch Errors early.
            valid_cmd_syntax, msg = CommandValidator.validate(comps)
            if not valid_cmd_syntax:
                print(comps)
                print(f"Invalid Command: {msg}")
                continue
            process_command(comps)
        except Exception as e:  # catching all exception here to avoid destroying state.
            print(e)
