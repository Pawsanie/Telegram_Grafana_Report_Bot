import json


class BotConfigParser:
    def __init__(self):
        self._config_file_path: str = ...
        self._bot_comfig = ConfigParser().read(
            filenames=self._config_file_path,
            encoding="UTF-8"
        )
