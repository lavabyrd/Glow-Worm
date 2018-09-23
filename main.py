import os
import json_format
import glow_logic
from flask import Flask, request, json, jsonify, make_response, render_template
from slackclient import SlackClient
from config import Config

# Creation of the Flask app
app = Flask(__name__)

app.config.from_object(Config)

# Addition of the tokens required. User_token may not be
# needed here unless we want to kick a user from the channel
b_token = app.config['BOT_TOKEN']
u_token = app.config['USER_TOKEN']
veri = app.config['VERIFICATION_TOKEN']
oauth_scope = app.config['OAUTH_SCOPE']
client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET']


# Global reference for the Slack Client tokens
sc = SlackClient(b_token)
sc_user = SlackClient(u_token)


# Points to the index page and just shows an easy way to
# determine the site is up
@app.route("/")
def index():
    return render_template('index.html')


# Endpoint for the slash command
@app.route("/glow", methods=["POST"])
def glow():
    payload = request.form.to_dict()
    # print(json_format.pretty_json(payload))
    channel_id = payload["channel_id"]
    user_list = sc.api_call("conversations.members", channel=channel_id)
    glow_logic.user_iteration.delay(user_list)
    return make_response("starting the glow!", 200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=False, host="0.0.0.0", port=port)
