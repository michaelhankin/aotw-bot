import os
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from pathlib import Path
from flask import Flask
from bot import Bot
from redis import Redis
from data import DataStore

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

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL is None or (REDIS_HOST is None and REDIS_PORT is None):
    raise EnvironmentError(
        "Either REDIS_URL or REDIS_HOST and REDIS_PORT environment variables must be set")

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_args = {'url': REDIS_URL} if REDIS_URL is not None else {
    'host': REDIS_HOST, 'port': REDIS_PORT}
r = Redis(**redis_args, password=REDIS_PASSWORD)
store = DataStore(r)
bot = Bot(slack_web_client, store)


@slack_events_adapter.on('app_mention')
def handle_mention(event_data):
    message = event_data["event"]
    bot.handle_message(message)


if __name__ == "__main__":
    app.run(port=3000)
