from os import path, sep
import json
"""
Contents config parser code.
"""


class BotConfigParser:
    """
    Parse raw configuration data for application objects.
    """
    def __init__(self):
        # Path settings:
        self.__replace_path_list: list[str] = [
            "Source_code", "Config_Parser.py"
        ]
        self.__root_path: str = f"{path.abspath(__file__).replace(path.join(*self.__replace_path_list), '')}"
        self._config_file_path: str = f"{self.__root_path}{sep}config.json"

        # Config settings:
        self._raw_data: dict = self._raw_config_load()
        self._telegram_bot_config: dict = self._raw_data["Telegram_Bot"]
        self._grafana_scraper_config: dict = self._raw_data["Grafana"]

    def _raw_config_load(self) -> dict:
        """
        Get raw application configuration data.
        :return: dict
        """
        with open(
                file=self._config_file_path,
                mode='r',
                encoding='utf-8'
        ) as json_file:
            return json.loads(
                json_file.read()
            )

    def get_telegram_bot_config(self) -> dict:
        """
        Get config for TelegramReportBot.
        :return: dict
        """
        return self._telegram_bot_config

    def get_grafana_scraper_config(self) -> dict:
        """
        Get config for GrafanaScraper.
        :return: dict
        """
        return self._grafana_scraper_config
