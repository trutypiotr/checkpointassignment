import os

from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from slack_sdk import WebClient

from myapp.sqs import send_message

app = App(
    token=os.getenv("BOT_SLACK_TOKEN"), signing_secret=os.getenv("SLACK_SINGING_SECRET")
)


@app.event("message")
def handle_message_events(body, say):
    event = body.get("event", {})
    text = event.get("text", "")
    ts = event.get("event_ts", "")
    channel = event.get("channel", "")
    send_message({"task": "check_patterns", "args": [text, ts, channel]})


slack_handler = SlackRequestHandler(app)
slack_client = WebClient(token=os.getenv("USER_SLACK_TOKEN"))
