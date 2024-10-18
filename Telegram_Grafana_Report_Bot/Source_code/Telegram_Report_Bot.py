from io import BytesIO
from datetime import datetime, timedelta
import logging
from asyncio import run

from aiohttp import ClientSession
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
"""
Contents Telegram Report Bot code.
"""


class TelegramReportBot:
    """
    Bot sending Grafana charts on request.
    """
    def __init__(
            self, *,
            bot_config: dict,
            handlers_configuration: dict
    ):
        """
        :param bot_config: Hash table with Telegram bot configuration data.
        :param handlers_configuration: Hash table with handlers data.
        """
        # Bot settings:
        self._bot_config: dict = bot_config
        self._handlers_configuration: dict = handlers_configuration
        self._start_time: float = datetime.now().timestamp()

        # Create bot session:
        self._telegram_bot: AsyncTeleBot = AsyncTeleBot(
            token=self._bot_config["token"]
        )

    def _send_massage(self, *, channel_id: str, message: str):
        """
        :param channel_id: Chanel id.
        :param message: Message for sending.
        """
        self._telegram_bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    @staticmethod
    async def _get_grafana_image(*, grafana_image_url: str, headers: dict) -> BytesIO:
        """
        Download grafana dashboard image for telegram message.
        :param grafana_image_url: Url without time.
        :return: BytesIO
        """
        async with ClientSession(
                headers=headers
        ) as session:
            async with session.get(
                    url=grafana_image_url,
                    allow_redirects=True
            ) as response:
                logging.log(
                    level=
                    logging.INFO if response.status == 200
                    else logging.WARNING,
                    msg=
                    f"Attempted to download image from url:\n{grafana_image_url}\n"
                    f"Status {response.status}"
                )
                if response.headers.get('Content-Type') != "image/png":
                    logging.error(
                        f"Attempted to download image from url:\n{grafana_image_url}\n"
                        "No image returned: possible authorization issues\n"
                        f"Response content: {response.headers.get('Content-Type')}"
                    )
                return BytesIO(
                    await response.read()
                )

    @staticmethod
    def _generate_grafana_url(grafana_raw_url) -> str:
        """
        Generate url for Grafana image render and response message.
        :param grafana_raw_url: Row url without time.
        """
        current_time: datetime = datetime.now()
        time_from: int = int(
            (
                    current_time - timedelta(hours=1)
            ).timestamp()
        )
        time_until: int = int(
            current_time.timestamp()
        )
        return grafana_raw_url.format(
            time_from,
            time_until
        )

    def _user_validator(self, message: Message) -> bool:
        """
        Determines whether the user has permission to write a message.
        :param message: Message object.
        :return: bool
        """
        # Message settings:
        chat_id: int = message.chat.id
        user_name: str = message.from_user.username

        # Exact time settings:
        if message.date < self._start_time:
            return False

        # Bot direct messages settings:
        dm_rules: tuple = (
                    message.chat.type == "private",
                    user_name in self._bot_config["dm_white_list"]
                )
        if dm_rules[0]:
            if not all(dm_rules):
                logging.warning(
                    "An unknown user attempted to write a private message."
                    f'\nUser name "{user_name}" not in "dm_white_list"!'
                    f'\nThe command called: "{message.text}"'
                )
                return False

        # In chanel bot interact settings:
        chanel_rules: tuple = (
            str(chat_id)[4:] in self._bot_config["channel_id"],
            user_name in self._bot_config["channel_white_list"]
        )
        if chanel_rules[0]:
            if not all(chanel_rules):
                logging.warning(
                    "A user who does not have privileges to interact with the bot attempted to call it in a channel."
                    f'\nUser name: "{user_name}'
                    f'\nChanel id: "{chat_id}"'
                    f'\nThe command called: "{message.text}"'
                )
                return False

        return True

    def bot_loop(self):
        """
        Registers handles and starts an infinite loop of bot.
        """
        # Generate handlers callbacks:
        for handler in self._handlers_configuration:
            async def grafana_handle(
                    message: Message,
                    handler_name: str
            ):
                if self._user_validator(message) is False:
                    return

                # Generate replay content:
                grafana_image_url: str = self._generate_grafana_url(
                    grafana_raw_url=self._handlers_configuration[
                        handler_name
                    ][
                        "url"
                    ]
                )
                get_image_data: BytesIO = await self._get_grafana_image(
                            grafana_image_url=grafana_image_url,
                            headers=self._handlers_configuration[
                                handler_name
                            ][
                                "request_header"
                            ]
                        )

                # Send message:
                await self._telegram_bot.send_photo(
                    chat_id=message.chat.id,
                    photo=get_image_data,
                    caption=
                    f"{self._handlers_configuration[handler_name]['handle_description']}",
                    # TODO: Now the mechanism for attaching a url link to a photo has been implemented...
                    # f'\n<a href="{grafana_image_url.replace("&", "&amp;")}">Link</a> to event in dashboard.',
                    parse_mode="HTML"
                )

            # Register handler:
            self._telegram_bot.register_message_handler(
                callback=lambda message, handler_name=handler: grafana_handle(
                    message, handler_name
                ),
                commands=[handler],
                content_types=['text']
            )

        # Generate welcome message:
        @self._telegram_bot.message_handler(
            commands=[
                "start",
                "help"
            ]
        )
        async def send_welcome(message):
            if self._user_validator(message) is False:
                return
            await self._telegram_bot.send_message(
                chat_id=message.chat.id,
                text=
                "Greetings from GrafanaReport Bot!"
                "\nUsing the following commands," 
                "\nyou can always access important metrics of your business.\n"
                "\nCommand examples:"
                "\n/start - repeat this message."
                "\n/help - will do the same."
                "\n/" +
                "\n/".join(
                    f'{handler_name} - {description}.'
                    for handler_name, description in zip(
                        self._handlers_configuration.keys(),
                        [
                            value["handle_description"] for value
                            in self._handlers_configuration.values()
                        ]
                    )
                          )
            )

        run(
            self._telegram_bot.polling()
        )
