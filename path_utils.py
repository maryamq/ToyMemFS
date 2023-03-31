""" Some utility functions for handling file paths. """
from pathlib import PurePosixPath


def resolve_dots(path: PurePosixPath) -> list[str]:
    """ A utility function to resolve ... in paths."""
    stack = []
    parts = path.parts
    for p in parts:
        if p == "..":
            if stack:
                stack.pop()
        else:
            stack.append(p)
    return stack


def merge_and_deconstruct(base: str, path_str: str) -> list[str]:
    """ Helper function to merge paths. Returns a list of path parts. """
    base_path = PurePosixPath(base)
    incr_path = PurePosixPath(path_str)
    # case 1: absolute path. Ingore base filepath.
    if incr_path.is_absolute():
        return incr_path.parts

    # Combine paths and resolve ... if needed.
    combined_path = base_path.joinpath(incr_path)
    return resolve_dots(combined_path)


# TODO(maryamq): Cleanup later. This is for quick testing.
if __name__ == "__main__":
    print("Absolute: ", merge_and_deconstruct("/", "/world"))
    print("Absolute: ", merge_and_deconstruct("/hello/adir", "/world"))
    print("Relative: ", merge_and_deconstruct("/hello", "world"))
    print("Dots: ", merge_and_deconstruct("/home/alone", "../invasion"))
    print("Dots: ", merge_and_deconstruct("/home/..", "invasion"))
