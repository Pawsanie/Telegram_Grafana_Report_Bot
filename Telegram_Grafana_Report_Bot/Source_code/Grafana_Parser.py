"""
Contents config grafana part parser code.
"""


class GrafanaParser:
    """
    Parse Grafana config part to ReportBot handler settings.
    """
    def __init__(self, grafana_config: dict):
        # Grafana settings:
        self._grafana_config: dict = grafana_config
        self._time_reference: str = "orgId=1&refresh=10s&from={}&to={}"
        self._panel_reference: str = "viewPanel={}&width={}&height={}"

    def get_handlers_settings(self) -> dict:
        """
        Generate handlers settings for TelegramReportBot.
        Used in TelegramGrafanaReportBot.
        :return: dict
        """
        return self._generate_handlers()

    def _generate_handlers(self) -> dict:
        """
        Parse handlers data from grafana config path.
        Generate handlers data for TelegramReportBot.
        :return: dict
        """
        handlers_collection: dict = {}
        for grafana_instance in self._grafana_config:
            for handler, handler_settings in grafana_instance["handlers"].items():
                handlers_collection.update(
                    {
                        handler: {
                            "url": self._generate_grafana_url(
                                grafana_url=grafana_instance["url"],
                                grafana_settings=handler_settings
                            ),
                            "request_header": {
                                "Accept": "image/png",
                                "Authorisation": f"Bearer {grafana_instance['token']}"
                            },
                            "handle_description": handler_settings["handle_description"]
                        }
                    }
                )
        return handlers_collection

    def _generate_grafana_url(
            self, *,
            grafana_url: str,
            grafana_settings: dict
    ) -> str:
        """
        Generate url for image download.
        :param grafana_url: Grafana url.
        :param grafana_settings: Hash table with handler configuration.
        :return: str
        """
        def setup_kiosk(kiosk_status: bool) -> str:
            if kiosk_status is True:
                return "&kiosk"
            else:
                return ""

        return \
            f"""
            {grafana_url}/render/d
            /{grafana_settings['dashboard_uid']}
            ?{self._time_reference}
            &{
                self._panel_reference.format(
                    grafana_settings['panel']['id'],
                    grafana_settings['panel']['width'],
                    grafana_settings['panel']['height']
                )
            }
            {setup_kiosk(grafana_settings['kiosk_status'])}
            """\
                .replace('\n', '')\
                .replace(' ', '')
