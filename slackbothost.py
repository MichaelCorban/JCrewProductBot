import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import chatbotpy311
import time

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)

@app.event("message")
def event_test(message, body, say, logger):
    logger.info(body)
    inpt = message['text']
    response = chatbotpy311.query(inpt)
    say(response)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods = ["POST"])
def slack_events():
    return handler.handle(request)
        
if __name__ == "__main__":
    flask_app.run(debug=True)
