import os
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from bot import Bot
import re

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
if SLACK_SIGNING_SECRET is None:
    raise EnvironmentError(
        "SLACK_SIGNING_SECRET environment variable must be set")
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if SLACK_BOT_TOKEN is None:
    raise EnvironmentError(
        "SLACK_BOT_TOKEN environment variable must be set")
slack_web_client = WebClient(token=SLACK_BOT_TOKEN)

bot = Bot(slack_web_client)


@slack_events_adapter.on('app_mention')
def handle_mention(event_data):
    message = event_data["event"]
    bot.handle_message(message)


if __name__ == "__main__":
    app.run(port=3000)
