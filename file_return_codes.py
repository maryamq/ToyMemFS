""" Class to encapsulate return codes from our filesystem.
"""


class FileReturnCodes:
    """ Helper for consistent error codes and messaging. 
    This exists mostly to save keystrokes.
    """

    # Constants representing various file-related errors.
    SUCCESS = 0
    ALREADY_EXIST = 1
    CREATION_SUCCESSFUL = 2
    INVALID_PATH = 3
    DELETE_FAILED = 4
    UNSUPPORTED = 5

    # Error templates.
    _error_tmpl = {
        SUCCESS: "{success_msg} {name}",
        ALREADY_EXIST: "{err_msg}: Already Exists: {name}",
        INVALID_PATH: "{err_msg}: Invalid path: {name} ",
        DELETE_FAILED: "{err_msg}: Deletion Failed. {name}}",
        UNSUPPORTED: "{err_msg}: UnSupported. {name}"
    }

    # Default values to populate the templates.
    template_defaults = {
        "success_msg": "Success! ",
        "err_msg": "Error! ",
        "name": "",
    }

    @classmethod
    def add_template(cls, error_code: int, template: str, **kw_defaults):
        """ Adds or overwrite custom templates. 
        This can be used to introduce custom error messages and codes.
        """
        FileReturnCodes._error_tmpl[error_code] = template
        if kw_defaults:
            FileReturnCodes.template_defaults.update(kw_defaults)

    @classmethod
    def print_message(cls, return_code, **kwargs) -> str:
        """ Generates an error message using the error code and kwargs.
         Arguments:
          return_code: int to represent a error code. 
          kwargs: string key-value args to populate the error template.
        """
        dict_args = FileReturnCodes.template_defaults.copy()
        dict_args.update(kwargs)
        print(FileReturnCodes._error_tmpl[return_code].format(
            **dict_args).strip())


# TODO(maryamq): Testing.. to be deleted.
if __name__ == "__main__":
    FileReturnCodes.print_message(FileReturnCodes.SUCCESS, name="mar")
    FileReturnCodes.add_template(10, "Hello {foo}", foo="bar")
    FileReturnCodes.print_message(10)
    FileReturnCodes.print_message(10, foo="custom foo")
