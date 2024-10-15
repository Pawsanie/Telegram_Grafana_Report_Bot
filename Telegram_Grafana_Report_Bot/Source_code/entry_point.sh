#!/bin/sh
# Shell script parse temporary config to standard configuration file for Bot pod.

# Workaround for Docker's File Inode Change Issue:
cat /application/temporary_config.json > /application/config.json

# Parse Bot config:
sed -i "s|\${TELEGRAM_CHANNEL_ID}|$TELEGRAM_CHANNEL_ID|g" /application/config.json
sed -i "s|\${TELEGRAM_BOT_TOKEN}|$TELEGRAM_BOT_TOKEN|g" /application/config.json
sed -i "s|\${TELEGRAM_BOT_DM_WHITE_LIST}|$TELEGRAM_BOT_DM_WHITE_LIST|g" /application/config.json
sed -i "s|\${GRAFANA_URL}|$GRAFANA_URL|g" /application/config.json
sed -i "s|\${GRAFANA_TOKEN}|$GRAFANA_TOKEN|g" /application/config.json
sed -i "s|\${TELEGRAM_BOT_CHANNEL_WHITE_LIST}|$TELEGRAM_BOT_CHANNEL_WHITE_LIST|g" /application/config.json

# Run application:
python -B ./Source_code/Telegram_Grafana_Report_Bot.py