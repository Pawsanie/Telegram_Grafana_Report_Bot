# Telegram Grafana Report Bot

The repository contains the source code of the Bot that sends users Grafana graphics upon request in channels or private messages in Telegram.<br>
The bot can interact with any number of handles from any number of Grafans.<br>
All of them are added through the JSON configuration.<br>

The repository also contains an example deployment for Docker-Compose.<br>
Including two test graphics.

## Disclaimer:
:warning:**Using** some or all of the elements of this code, **You** assume **responsibility for any consequences!**<br>

:warning:The **licenses** for the technologies on which the code **depends** are subject to **change by their authors**.<br><br>

## Contents:
### Dependencies:
* [Required](#Required)
* [Required Packages](#Required-Packages)
* [Installing the Required Packages](#Installing-the-Required-Packages)

### Pre-deployment steps:
* [Telegram Bot registration](#Telegram-Bot-registration)
* [Telegram channel settings](#Telegram-channel-settings)
* [Crate Grafana Technical User](#Crate-Grafana-Technical-User)
* [Add new handlers to Config file](#Add-new-handlers-to-Config-File)

### Deployment:
* [Deploy with Docker-Compose](#Deploy-with-Docker-Compose)
* [Run on Bare-Metal or Virtual Machine](#Run-on-Bare-Metal-or-Virtual-Machine)
* Run on local machine: see th paragraph above.

### Interacting with the Bot:
* [How to call the Bot](#How-to-call-the-Bot)

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

**pyTelegramBotAPI** [GPL-2.0 license]:
* :octocat:[pyTelegramBotAPI GitHub](https://github.com/eternnoir/pyTelegramBotAPI)
* :bookmark_tabs:[pyTelegramBotAPI pypi internet page](https://pypi.org/project/pyTelegramBotAPI/)
Used to interact with the telegram api

## Installing the Required Packages:
```bash
pip install aiohttp
pip install pyTelegramBotAPI
```

## Pre-deployment steps

### Telegram Bot registration:
To start the bot registration process, you must **have** a [Telegram](https://telegram.org/) **account**.
* **Log in** to Telegram in any way convenient for you and write to the **[@BotFather](https://t.me/BotFather)** bot.<br>
* Write to the bot:
    ```text
    /start
    ```
* Next write him:
    ```text
    /newbot
    ```
* After that, write what your bot will be called. This name will be **displayed** as its name in the **profile**.<br>
Then you will need to write the **unique bot ID**, according to the **instructions**.<br>
As a result, you will receive a unique **token** for your bot. It will be needed for program **configuration** file.<br>
More details about its use can be found in paragraphs «[Deploy-with-Docker-Compose](#Deploy-with-Docker-Compose)» and «[Run on Bare-Metal or Virtual Machine](#Run-on-Bare-Metal-or-Virtual-Machine)».

### Telegram channel settings:
Create a channel in Telegram in any way convenient for you.
* Add your bot to the channel and make him an administrator in it.<br>
Remove all unnecessary rights from him: the ability to write messages to the channel is enough.
* Open Telegram [Web-version](https://web.telegram.org/)<br>
Find your chanel and copy **channel id** in web url after **#-** symbols.<br>
As exemple **#-0000000000**.<br>
It will be needed for program **configuration** file.
* More details about its use can be found in paragraphs «[Deploy with Docker-Compose](#Deploy-with-Docker-Compose)» and «[Run on Bare-Metal or Virtual Machine](#Run-on-Bare-Metal-or-Virtual-Machine)».

### Crate Grafana Technical User:
The creation process will be described for version **11.2.2**. In other versions the interface may change.<br>
But it most likely will not change in the future.
* Open your Grafana web interface.
* On the left side of the page, select **Administration**.
* Select **Users and access**.
* Next select **Service accounts**.
* In the upper right part of the page, click "**Add service account**".
* Enter a descriptive **name** under which you will be able to easily find this service account in the list of others.<br>
And select **Viewer** rights for him.
* On the right side, in the token table, click "**Add service account token**".<br>
* Click "**Generate token**"<br>
Be sure to **copy the token immediately** after this.<br>
It will only be **shown once**.<br>
It will be needed for program **configuration** file.<br>
More details about its use can be found in paragraphs «[Deploy with Docker-Compose](#Deploy-with-Docker-Compose)» <br>
and «[Run on Bare-Metal or Virtual Machine](#Run-on-Bare-Metal-or-Virtual-Machine)».

### Add new handlers to Config file:
Since the complete filling of the configuration file depends on how you will **deploy** the application, <br>
let's first look at how to add **handlers** for the Bot.<br>
**Config file location:**<br>
**./**:open_file_folder:Telegram_Grafana_Report_Bot<br>
   └── :page_facing_up:config.json<br>
**Example of handler in config.json file:**
```json
{
    "Grafana": [
        {
          "token": "${GRAFANA_TOKEN}",
          "url": "${GRAFANA_URL}",
          "handlers": {
            
            "e1": {
              "dashboard_uid": "ee0jj9k1l8zr4d",
              "kiosk_status": true,
              "time_zone": "Europe%2FMoscow",
              "panel": {
                "id": 1,
                "width": 560,
                "height": 480
              },
              "handle_description": "Example dashboard 01"
            },
            ...
            
          }
        },
      {...}
    ]
}
```
* **token** - the value of this key is a token with which the bot can connect to Grafana.<br>
More details on how to get this token were written above, in paragraph «[Crate Grafana Technical User](#Crate-Grafana-Technical-User)».<br>
When to replace the default value is described in the «[Deployment](#Deployment)» paragraph.<br>
However, it is important to mention now that this value is unique for each Grafana you want to use.
* **url** - it can be either an IP address or a DNS name, depending on your settings.<br>
When to replace the default value is described in the «[Deployment](#Deployment)» paragraph.<br>
Similar to the previous key, this value will be unique for each Grafana you want to use.<br>
Below is an example of an url link from where you can get this value for configuration if necessary.
* **Handlers** - the value of this key is a nested dictionary that **lists all handles** settings.<br>
The embedded key is the **handle** itself that the user will need to call.<br>
In this example it is called "**e1**".<br>
Accordingly, it will be called in the chat with the bot by the command "**/e1**".<br>
You need to come up with this value yourself.
  * **dashboard_uid** - this is a unique identifier of the dashboard in Grafana.<br>
The name of the dashboard and graph, although mentioned in the URL, does not really matter and may not even be added.<br>
Only this parameter and the panel ID have matter.<br>
Below is an example of an **url** link where you can **get** this value from your graph.
  * **kiosk_status** - is responsible for whether to show the Grafana interface when rendering an image, or not.<br>
Value is a **boolean** constant.
  * **time_zone** - responsible for which time zone to generate graphs.<br>
You can choose any convenient standard time zone.<br>
Their list is in Grafana.<br>
To open it, click on the time settings for which to display graphs in the upper right corner.<br>
Click "**Change time settings**"<br>
Next click "**Type to search...**"<br>
Time zones are determined by the format **Country/City**.<br>
You need to swap **/** symbol to **%2F**.<br>
You can also write IANA by analogy. As example **Etc%2FUTC**.
  * **panel** - the panel is the actual graph that is being drawn.<br>
Each dashboard can have multiple panels, each with its own number.<br>
The key value is a nested dictionary describing the panel.
    * **id** - is responsible for which graph to draw.<br>
Below is an example of an **url** link where you can **get** this value from your graph.
    * **width** - width of the generated image.<br>
You need to come up with this value yourself.
    * **height** - height of the generated image.<br>
You need to come up with this value yourself.
  * **handle_description** - a description of each will be generated in the welcome message <br>
and added to each picture in caption, for ease of searching through messages.<br>
You need to come up with this value yourself.

All the settings described above, except for the token, are responsible for the link that will return the image to us.<br>
For simplicity, they are substituted in the example:<br>
**url**:3000/render/d/**dashboard_uid**/dashboard_name?orgId=1&refresh=10s&from=time&to=time&viewPanel=**id**&width=**with**&height=**height**&tz=**time_zone**&**kiosk_status**<br>
Please note that organization ID generation is not implemented.<br>
Its **value** is hardcoded as **1**.

## Deployment

### Deploy with Docker-Compose:

The repository contains a test example that will deploy with a sample of Grafana for an example of using the bot,<br>
a Grafana render container, and 2 graphs.<br>
However, you will have to customize one or more files.

**Files location:**<br>
**./**:open_file_folder:Telegram_Grafana_Report_Bot<br>
   ├── :file_folder:Docker<br>
   │        ├── :page_facing_up:.env<br>
   │        └── :page_facing_up:docker-compose.yml<br>
   ├── :file_folder:Source_code<br>
   │        └── :page_facing_up:entry_point.sh<br>
   └── :page_facing_up:config.json<br>

First, you need to create a "**.env**"" file with environment variables to add to the "**Docker**" folder.<br>
**.env file example:**<br>
```text
# .env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=...,...
TELEGRAM_BOT_DM_WHITE_LIST=...,...
TELEGRAM_BOT_CHANNEL_WHITE_LIST=...,...,...

GRAFANA_TOKEN=...
GRAFANA_URL=http://example_grafana:3000
GRAFANA_RENDER_SERVER_URL=http://grafana_renderer:8081/render
GRAFANA_ADMIN_USER=...
GRAFANA_ADMIN_PASSWORD=...
```
* TELEGRAM_BOT_DM_WHITE_LIST - List of names of trusted users in telegram, written separated by commas without spaces.
* TELEGRAM_BOT_CHANNEL_WHITE_LIST - List of names of trusted users in telegram, written separated by commas without spaces.

* TELEGRAM_BOT_TOKEN - The **token** we received by performing the steps in «[Telegram Bot registration](#Telegram-Bot-registration)».
* TELEGRAM_CHANNEL_ID - «[Telegram channel settings](#Telegram-channel-settings)»
* GRAFANA_TOKEN - The **token** we received by performing the steps in «[Crate Grafana Technical User](#Crate-Grafana-Technical-User)».
* GRAFANA_URL - ip address or DNS name of yore Grafana instance.
* GRAFANA_RENDER_SERVER_URL - ip address or DNS name of yore Grafana-Render instance.
* GRAFANA_ADMIN_USER - name of Grafana root user.
* GRAFANA_ADMIN_PASSWORD - Grafana root user password.
Each instance of your Grafana or render servers needs its own environment variables.<br>
Additional instances will also need to be added in **docker-compose.yaml** and **entry_point.sh**.<br>
How to add new handles, including grafana instances, can be read in the «[Add new handlers to Config file](#Add-new-handlers-to-Config-file) paragraph)».

There is no point in describing the structure of these files in more detail, <br>
since you will literally need to make duplicates of these variables for new grafana instances, but under different names.<br>
If you do not want to use more than one Grafana, you just need to replace the data in the file with your own, according to the rules described above.

**Example of using Docker variables in config.json file:**<br>
```json
{
  "Telegram_Bot":
  {
    "token": "${TELEGRAM_BOT_TOKEN}",
    "dm_white_list": [
      "${TELEGRAM_BOT_DM_WHITE_LIST}"
    ],
    "channel_id": [
      "${TELEGRAM_CHANNEL_ID}"
    ],
    "channel_white_list": [
      "${TELEGRAM_BOT_CHANNEL_WHITE_LIST}"
    ],
    "block_forwarding_messages": true
  },

  "Grafana": [
    {
      "token": "${GRAFANA_TOKEN}",
      "url": "${GRAFANA_URL}",
      "handlers": {...}
    }
  ]
}
```
More details about the keys and values of the file can be found in the next paragraph «[Run on Bare-Metal or Virtual Machine](#Run-on-Bare-Metal-or-Virtual-Machine)», with example values.<br>

To run Docker-compos, open terminal and go to the Docker directory and enter the command.
```shell
docker-compose up -d
```

### Run on Bare-Metal or Virtual Machine:

For normal launch primarily you will need to manually configure the **config.json** file.<br>
Then you will need to launch the entry point to the program.

**Files location:**<br>
**./**:open_file_folder:Telegram_Grafana_Report_Bot<br>
   ├── :file_folder:Source_code<br>
   │        └── :page_facing_up:Telegram_Grafana_Report_Bot.py<br>
   └── :page_facing_up:config.json<br>

**Example of config.json file:**
```json
{
  "Telegram_Bot":
  {
    "token": "0000000000:aAaAaAaaAaAaAaAaAaAaaaAAAaAaAaAAaaAa",
    "dm_white_list": [
      "dm_user",
      "dm_user2"
    ],
    "channel_id": [
      "0000000000",
      "0000000000"
    ],
    "channel_white_list": [
      "dm_user",
      "channel_user"
    ],
    "block_forwarding_messages": true
  },

  "Grafana": [
    
    {
      "token": "glsa_A0A0aA0aAaA0A0aA0aAaA0A0aA0aA_00ffAaaa",
      "url": "http://example_grafana:3000",
      "handlers": {...}
    }
    
  ]
}
```

Run **Telegram_Grafana_Report_Bot.py** with command:
```shell
python -B Telegram_Grafana_Report_Bot.py
```

## How to call the Bot:

Go to the channel where your bot is located, or start a private message conversation with it.<br>
Use one of the commands:
* **/star** - generate welcome message with all handles description. 
* **/help** - will do the same.
* **/all** - get all graphs images from all Grafans related to the handles you added.
* **Graph handler** - es example **/e1** in example Docker-compose.

***

:hearts: **Thank you** for your interest in my work! :hearts:<br><br>