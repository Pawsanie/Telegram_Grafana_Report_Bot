from telebot import TeleBot


class TelegramReportBot:
    def __init__(self):
        ...
        # self._tele_bot: TeleBot = TeleBot(
        #     token=...
        # )

        while True:
            pass

    def _send_massage(self, *, channel_id: str, message: str):
        """
        :param channel_id:
        :param message:
        :return:
        """
        self._tele_bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
