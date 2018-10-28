import os
import json_format
import glow_logic
import responder
from flask import Blueprint, Flask, request, json, jsonify, make_response
from slackclient import SlackClient


# Register the responder API object
api_r = responder.API()

# Register blueprint
api = Blueprint('api', __name__, template_folder='templates')


# Endpoint for the slash command
@api.route("/glow", methods=["POST"])
def glow():
    payload = request.form.to_dict()
    # print(json_format.pretty_json(payload))

    @api_r.background.task
    def lookup(payload):
        channel_id = payload["channel_id"]
        b_token = os.environ.get('GLOW_BOT_TOKEN')
        sc = SlackClient(b_token)
        user_list = sc.api_call("conversations.members", channel=channel_id)
        glow_logic.user_iteration(user_list)

    lookup(payload)
    return make_response("starting the glow!", 200)
