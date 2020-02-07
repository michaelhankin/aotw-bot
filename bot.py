class Bot:
    def __init__(self, slack_client):
        self.slack_client = slack_client

    def handle_message(self, message):
        if "hi" in message.get("text"):
            channel = message["channel"]
            message = "Hello <@%s>!" % message["user"]
            self.slack_client.chat_postMessage(channel=channel, text=message)
