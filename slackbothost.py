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
#client.chat_postMessage(channel='#general', text="Hello")

#app = Flask(__name__)
app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)
#slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

@app.event("message")
def event_test(message, body, say, logger):
    logger.info(body)
    print(message['text'])
    #say("what's up?")
    inpt = message['text']
    response = chatbotpy311.query(inpt)
    say(response)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods = ["POST"])
def slack_events():
    return handler.handle(request)

'''
@slack_event_adapter.on('message')
def message(payload):
    #print(payload)
    print("hi")
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    type = event.get('type')

    if BOT_ID != user_id:
        inpt = text
        #client.chat_postMessage(channel=channel_id, text=chatbotpy311.query(inpt))
        response = chatbotpy311.test(inpt)
        client.chat_postMessage(channel=channel_id, text=response)
'''
        
if __name__ == "__main__":
    flask_app.run(debug=True)