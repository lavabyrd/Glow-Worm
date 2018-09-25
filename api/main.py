import os
import json_format
import glow_logic
from flask import Blueprint, Flask, request, json, jsonify, make_response
from slackclient import SlackClient


# Register blueprint
api = Blueprint('api', __name__, template_folder='templates')


# Global reference for the Slack Client tokens

b_token = os.environ.get('GLOW_BOT_TOKEN')
sc = SlackClient(b_token)


# Endpoint for the slash command
@api.route("/glow", methods=["POST"])
def glow():
    payload = request.form.to_dict()
    # print(json_format.pretty_json(payload))
    channel_id = payload["channel_id"]
    user_list = sc.api_call("conversations.members", channel=channel_id)
    glow_logic.user_iteration.delay(user_list)
    return make_response("starting the glow!", 200)
