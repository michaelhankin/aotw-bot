import json
import random
import re
from urllib.parse import urlparse

INVALID_COMMAND_ERROR = 'Invalid command. I support the following commands: `nominate`, `ping`.'
INVALID_NOMINATION_COMMAND_ERROR = 'Invalid nomination command. I can only accept nominations in the format `nominate <link to album>`.'
INVALID_NOMINATION_ERROR = 'Invalid nomination. I only accept Spotify URLs as nominations at the moment.'


def get_slack_display_name(slack_client, user_id):
    return slack_client.users_info(
        user=user_id)['user']['profile']['display_name']


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
                self.handle_error(channel, INVALID_NOMINATION_COMMAND_ERROR)
                return

            user = message['user']
            nomination = tokens[2]

            self.handle_nomination(channel, user, nomination)
        elif command == 'list':
            if len(tokens) > 2:
                self.handle_error(channel, INVALID_COMMAND_ERROR)
                return

            self.handle_list_nominations(channel)
        elif command == 'select':
            if len(tokens) > 2:
                self.handle_error(channel, INVALID_COMMAND_ERROR)
                return

            self.handle_select_winner(channel)
        elif command == 'winners':
            if len(tokens) > 2:
                self.handle_error(channel, INVALID_COMMAND_ERROR)
                return

            self.handle_list_winners(channel)
        elif command == 'ping':
            if len(tokens) > 2:
                self.handle_error(channel, INVALID_COMMAND_ERROR)
                return

            response = "PONG"
            self.slack_client.chat_postMessage(channel=channel, text=response)
        else:
            self.handle_error(channel, INVALID_COMMAND_ERROR)

    def handle_nomination(self, channel, user, nomination):
        # Unpack Slack's formatted URL
        url = urlparse(nomination[1:-1].split('|')[0])
        parts = url.netloc.split('.')

        # As of right now, we expect `nomination` to be a Spotify URL
        if len(parts) < 3 or not parts[1] == 'spotify':
            self.handle_error(channel, INVALID_NOMINATION_ERROR)
            return

        result = self.data_store.save_nomination(nomination, user)
        if result == 1:
            message = 'Nomination saved!'
        else:
            message = f'Oops, you\'ve already nominated an album this week, <@{user}>.'
        self.slack_client.chat_postMessage(channel=channel, text=message)

    def handle_list_nominations(self, channel):
        result = self.data_store.list_nominations()

        if len(result) == 0:
            message = 'No nominations yet.'
        else:
            nominations_list = '\n'

            for user_id, nomination in result.items():
                user_id = user_id.decode('utf-8')
                nomination = nomination.decode('utf-8')

                username = get_slack_display_name(self.slack_client, user_id)
                nominations_list += f'- {nomination} nominated by {username}\n'

            message = f'Current list of nominations:\n{nominations_list}'
        self.slack_client.chat_postMessage(channel=channel, text=message)

    def handle_select_winner(self, channel):
        nominations = self.data_store.list_nominations()

        if len(nominations) == 0:
            message = 'No nominations yet.'
        else:
            winner = random.choice(list(nominations.items()))

            user_id = winner[0].decode('utf-8')
            nomination_url = winner[1].decode('utf-8')

            username = get_slack_display_name(self.slack_client, user_id)
            message = f'The winner is {nomination_url} nominated by {username}!'

            self.data_store.store_winner(user_id, nomination_url)
            self.data_store.clear_nominations()

        self.slack_client.chat_postMessage(
            channel=channel, text=message)

    def handle_list_winners(self, channel):
        winners = self.data_store.list_winners()

        if len(winners) == 0:
            message = 'No winners yet.'
        else:
            winners_list = '\n'

            for entry in winners:
                user, nomination = entry.decode('utf-8').split(' ')
                user = get_slack_display_name(
                    self.slack_client, user)

                winners_list += f'- {nomination} nominated by {user}\n'

            message = f'Past winners:\n{winners_list}'

        self.slack_client.chat_postMessage(channel=channel, text=message)

    def handle_error(self, channel, error_message):
        self.slack_client.chat_postMessage(channel=channel, text=error_message)
