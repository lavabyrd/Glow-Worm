import os
from flask import Flask, request, json, jsonify, make_response
from slackclient import SlackClient

VERIFICATION_TOKEN = os.environ.get("GLOW_VERIFICATION_TOKEN")
BOT_TOKEN = os.environ.get("GLOW_BOT_TOKEN")
USER_TOKEN = os.environ.get("GLOW_USER_TOKEN")

app = Flask(__name__)

sc = SlackClient(BOT_TOKEN)
sc_user = SlackClient(USER_TOKEN)

glow_start = "welcome to Glow worm!"


def pretty_json(json_data):
    """
    easily readable JSON
    stolen from Benoit's app!
    """
    return json.dumps(
        json_data, sort_keys=True, indent=4, separators=(',', ': ')
    )


@app.route("/glow", methods=["POST"])
def glow():
    payload = request.form.to_dict()
    print(pretty_json(payload))
    channel_id = payload["channel_id"]
    user_list = sc.api_call("conversations.members", channel=channel_id)
    for i in user_list['members']:
        # UB43F512L is the bot
        # U938A515W is specious
        if i == "UB43F512L":
            print(f"skipping {i}")

        else:
            sc.api_call("chat.postMessage", channel=i, token=BOT_TOKEN,
                        text=f"hey <@{i}>! here we glow!", as_user="true")
    return make_response("starting the glow!", 200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, host="0.0.0.0", port=port)
