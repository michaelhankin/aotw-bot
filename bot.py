INVALID_COMMAND_ERROR = 'Invalid command! Supported commands are: `nominate`, `ping`.'
INVALID_NOMINATION_ERROR = 'Invalid nomination format! Nominations must be in the format `nominate <link to album>`.'


class Bot:
    def __init__(self, slack_client, data_store):
        self.slack_client = slack_client
        self.data_store = data_store

    def handle_message(self, message):
        channel = message['channel']
        text = message.get('text', None)
        if text is None:
            self.handle_error(channel, INVALID_COMMAND_ERROR)
            return

        tokens = text.split(' ')
        command = tokens[1]

        if command == 'nominate':
            if len(tokens) > 3:
                self.handle_error(channel, INVALID_NOMINATION_ERROR)
                return

            user = message['user']
            nomination = tokens[2]
            self.handle_nomination(channel, user, nomination)
        elif command == 'ping':
            if len(tokens) > 2:
                self.handle_error(channel, INVALID_COMMAND_ERROR)
                return

            response = "PONG"
            self.slack_client.chat_postMessage(channel=channel, text=response)
        else:
            self.handle_error(channel, INVALID_COMMAND_ERROR)

    def handle_nomination(self, channel, user, nomination):
        result = self.data_store.save_nomination(nomination, user)
        if result == 1:
            message = 'Nomination saved!'
        else:
            message = f'Oops, you\'ve already nominated an album this week, <@{user}>'
        self.slack_client.chat_postMessage(channel=channel, text=message)

    def handle_error(self, channel, error_message):
        self.slack_client.chat_postMessage(channel=channel, text=error_message)
