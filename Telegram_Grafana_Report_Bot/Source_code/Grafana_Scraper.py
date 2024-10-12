from asyncio import run, gather

from aiohttp import ClientSession


class GrafanaScraper:
    def __init__(self, *, grafana_token: str, ):
        self._example: dict[str] = {
            'https://grafana.com': {
                "uid": "sadsda",
                "protocol": "https",
                "day_type": "d-solo",
                "kiosk_status": True,
                "time_zone": "Europe%2FMoscow"
            }
        }

        # Grafana settings:
        self._grafana_token: str = grafana_token
        self._request_headers: dict = {
            "Accept": "application/json",
            "Authorisation": f"Bearer {self._grafana_token}"
        }

        # Grafana url: settings:
        self._time_reference: str = "orgId=1&refresh=10s&from={}&to={}"
        self._panel_reference: str = "panelId={}&width={}&height={}"

    def _generate_grafana_urls(self):
        for grafana_url in self._example:
            def setup_kiosk(kiosk_status: bool) -> str:
                if kiosk_status is True:
                    return "&kiosk"
                else:
                    return ""

            self._dashbord_download_url: str = \
                f"{grafana_url}/render" \
                f"/{self._example['day_type']}" \
                f"/{self._example['uid']}" \
                f"?{self._time_reference.format(self._time_from, self._time_until)}" \
                f"&{self._panel_reference.format()}" \
                f"{setup_kiosk(self._example['kiosk_status'])}"


