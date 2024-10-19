# Telegram Grafana Report Bot

The repository contains the source code of the Bot that sends users Grafana graphics upon request in channels or private messages in Telegram.<br>
The bot can interact with any number of handles from any number of Grafans.<br>
All of them are added through the JSON configuration.<br>

The repository also contains an example deployment for Docker-Compose.<br>
Including 2 test charts.

## Disclaimer:
:warning:**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br>

:warning:The **licenses** for the technologies on which the code **depends** are subject to **change by their authors**.<br><br>

___
<br>

## Required:
The application code is written in python and obviously depends on it.<br>
**Python** version 3.10 [Python Software Foundation License / (with) Zero-Clause BSD license]:
* :octocat:[Python GitHub](https://github.com/python)
* :bookmark_tabs:[Python internet page](https://www.python.org/)

## Required Packages:
**aiohttp** [Apache License version 2.0]:
* :octocat:[Aiohttp GitHub](https://github.com/aio-libs/aiohttp)
* :bookmark_tabs:[Aiohttp pypi internet page](https://pypi.org/project/aiohttp/)

Used to perform asynchronous requests.

## Installing the Required Packages:
```bash
pip install aiohttp
```

**pyTelegramBotAPI** [GPL-2.0 license]:
* :octocat:[pyTelegramBotAPI GitHub](https://github.com/eternnoir/pyTelegramBotAPI)
* :bookmark_tabs:[pyTelegramBotAPI pypi internet page](https://pypi.org/project/pyTelegramBotAPI/)

Used to interact with the telegram api

## Installing the Required Packages:
```bash
pip install pyTelegramBotAPI
```