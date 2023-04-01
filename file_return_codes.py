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

    @classmethod
    def _get_default_tmpl_param_names(cls):
        """ Returns the defaults value for template params.
        """
        return {
            "success_msg": "Success! ",
            "err_msg": "Error! ",
            "name": "",
        }

    @classmethod
    def print_message(cls, return_code, **kwargs) -> str:
        """ Generates an error message using the error code and kwargs.
         Arguments:
          return_code: int to represent a error code. 
          kwargs: string key-value args to populate the error template.
        """
        dict_args = FileReturnCodes._get_default_tmpl_param_names()
        dict_args.update(kwargs)
        print(FileReturnCodes._error_tmpl[return_code].format(
            **dict_args).strip())
