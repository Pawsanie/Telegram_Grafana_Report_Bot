import logging

from Logger import logging_config, text_for_logging
from Grafana_Scraper import GrafanaScraper
from Telegram_Report_Bot import TelegramReportBot
"""
Contains the entry point code for the program.
"""


class TelegramGrafanaReportBot:
    def __init__(self):
        self._report_bot: TelegramReportBot = TelegramReportBot()
        # self._grafana_scraper: GrafanaScraper = GrafanaScraper(
        #     grafana_token=...
        # )

    def run(self):
        ...


if __name__ == "__main__":
    logging_config(
        log_path="logg_file.txt",
        log_level=30
    )
    try:
        TelegramGrafanaReportBot().run()
    except Exception as error:
        logging.critical(
            text_for_logging(
                log_text="The program launch ended with an error!",
                log_error=error
            )
        )
        raise error
