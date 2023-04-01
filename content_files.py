from io import StringIO
from base_file import FileType, BaseFile
from directory import Directory
from logging_utils import FileReturnCodes


class TextFile(BaseFile):
    _default_config = {
        "write_mode": "overwrite" # supported: overwrite | append
    }
    def __init__(self, name: str, parent: Directory):
        super().__init__(name, FileType.TEXT_FILE, parent)
        self._content = StringIO()

    def __iter__(self):
        self._content.flush()
        return iter(self._content)

    def is_empty(self):
        return len(self._content) == 0

    def add_content(self, content, **kwargs):
        config = TextFile._default_config
        if kwargs:
            config.update(kwargs)
        if config["write_mode"] == "append":
            self._content.writelines(content)
        else:
            # overwrite
            self._content.truncate(0)
            self._content.writelines(content)

    def __str__(self)->str:
        return self._content.getvalue()

    def delete(self) -> int:
        self._content.close()
        super().delete()
