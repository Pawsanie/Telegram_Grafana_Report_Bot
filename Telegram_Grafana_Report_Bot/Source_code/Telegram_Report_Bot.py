from io import BytesIO
from datetime import datetime, timedelta
import logging
from asyncio import run

from aiohttp import ClientSession
from telebot.async_telebot import AsyncTeleBot


class TelegramReportBot:
    def __init__(
            self, *,
            bot_config: dict,
            handlers_configuration: dict
    ):
        """
        ...
        :param bot_config:
        :param handlers_configuration:
        """
        self._bot_config: dict = bot_config
        self._handlers_configuration: dict = handlers_configuration

        self._telegram_bot: AsyncTeleBot = AsyncTeleBot(
            token=self._bot_config["token"]
        )

    def _send_massage(self, *, channel_id: str, message: str):
        """
        :param channel_id:
        :param message:
        """
        self._telegram_bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    @staticmethod
    async def _get_grafana_image(*, grafana_raw_url: str, headers: dict) -> BytesIO:
        """
        Download grafana dashboard image for telegram message.
        :param grafana_raw_url: Url without time.
        :return: BytesIO
        """
        async def download_file(image_url):
            async with ClientSession(
                    headers=headers
            ) as session:
                async with session.get(url=image_url) as response:
                    response.raise_for_status()
                    return await response.read()

        # Generate Grafana image url:
        current_time: datetime = datetime.now()
        time_from: int = int(
            (
                    current_time - timedelta(hours=1)
            ).timestamp()
        )
        time_until: int = int(
            current_time.timestamp()
        )
        grafana_image_url: str = grafana_raw_url.format(
            time_from,
            time_until
        )

        logging.error(grafana_image_url)

        # Download Grafana dashboard image:
        grafana_dashboard_image: bytes = await download_file(grafana_image_url)
        return BytesIO(grafana_dashboard_image)

    def bot_loop(self):
        for handler in self._handlers_configuration:
            async def _grafana_handle(message):
                chat_id: str = message.chat.id
                chat_type: str = message.chat.type
                user_name: str = message.from_user.username

                # if chat_id[4:] not in self._bot_config["channel_id"] \
                #         or chat_type != "private":
                #     logging.warning("User cant chatting")
                #     return
                # if message.chat.type == "private" \
                #         and user_name not in self._bot_config["dm_white_list"]:
                #     logging.warning("chat dm but user not in wl")
                #     return
                # if chat_type != "private" \
                #         and user_name not in self._bot_config["channel_white_list"]:
                #     logging.warning("chat tipe is not private or user not in wl")
                #     returnW

                get_image_data: BytesIO = await self._get_grafana_image(
                            grafana_raw_url=self._handlers_configuration[handler]["url"],
                            headers=self._handlers_configuration[handler]["request_header"]
                        )
                grafana_dashboard_image: str = get_image_data.getvalue().decode('utf-8')
                await self._telegram_bot.send_photo(
                    chat_id=chat_id,
                    photo=grafana_dashboard_image
                )
            self._telegram_bot.register_message_handler(
                callback=_grafana_handle,
                commands=[handler],
                content_types=['text']
            )

        @self._telegram_bot.message_handler(
            commands=[
                "start",
                "help"
            ]
        )
        async def send_welcome(message):
            await self._telegram_bot.send_message(
                chat_id=message.chat.id,
                text="Good Day!"
                     "\nCommand examples:"
                     "\n/start"
                     "\n/help"
                     + "\n/".join(
                        self._handlers_configuration.keys()
                     )
            )

        run(
            self._telegram_bot.polling()
        )
