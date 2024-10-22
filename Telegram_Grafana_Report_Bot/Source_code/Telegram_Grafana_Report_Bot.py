import logging

from Logger import logging_config, text_for_logging
from Config_Parser import BotConfigParser
from Grafana_Parser import GrafanaParser
from Telegram_Report_Bot import TelegramReportBot
"""
Contains the entry point code for the program.
"""


class TelegramGrafanaReportBot:
    def __init__(self):
        # Parse config:
        self._config_parser: BotConfigParser = BotConfigParser()

        # Grafana settings:
        self._grafana_scraper: GrafanaParser = GrafanaParser(
            self._config_parser.get_grafana_parser_config()
        )

        # Telegram bot settings:
        self._report_bot: TelegramReportBot = TelegramReportBot(
            bot_config=self._config_parser.get_telegram_bot_config(),
            handlers_configuration=self._grafana_scraper.get_handlers_settings()
        )

        # Run loop:
        self._report_bot.bot_loop()


if __name__ == "__main__":
    logging_config(
        log_path="logg_file.txt",
        log_level=30
    )
    try:
        TelegramGrafanaReportBot()
    except Exception as error:
        logging.critical(
            text_for_logging(
                log_text="The program launch ended with an error!",
                log_error=error
            )
        )
        raise error
