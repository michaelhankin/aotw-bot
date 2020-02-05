import os
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# TODO: throw exceptions when required env vars are undefined
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_web_client = WebClient(token=slack_bot_token)


@slack_events_adapter.on('app_mention')
def handle_mention(event_data):
    message = event_data["event"]

    if "hi" in message.get("text"):
        channel = message["channel"]
        message = "Hello <@%s>!" % message["user"]
        slack_web_client.chat_postMessage(channel=channel, text=message)


slack_events_adapter.start(port=3000)
