# aotw-bot

⚠️ **WIP** ⚠️

aotw-bot is a Slack bot which runs an album of the week competition for your team.

## Running locally

Ensure that you have Python 3.7.x and Pipenv installed. Then:

```shell
# Clone this repo
git clone https://github.com/michaelhankin/aotw-bot.git

# Navigate into the repo
cd aotw-bot

# Create your .env
cp .env.example .env

# Update the values in .env in the text editor of your choice
# ...

# Install dependencies
pipenv install

# Launch the virtual environment for the app
pipenv shell

# Run the app
flask run
```

See [this guide](https://github.com/slackapi/python-slack-events-api#--development-workflow) for help connecting the bot to a Slack app in your workspace.
