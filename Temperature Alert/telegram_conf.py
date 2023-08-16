"""Configurations for telegram_alert.py"""
bolt_api_key = ""                 # This is your Bolt Cloud API Key
device_id = "BOLT1115198"                    # This is the device ID and will be similar to BOLTXXXX where XXXX is some numbers
telegram_chat_id = "@temp_alert_bolt_iot"            # This is the channel ID of the created Telegram channel. Paste after @ symbol.
telegram_bot_id = ""           # This is the bot ID of the created Telegram Bot. Paste after bot text.
threshold = 250                       # Threshold beyond which the alert should be sent
message0 = "Alert! Sensor value has exceeded " + str(threshold) + ". The current value is " + str(threshold)