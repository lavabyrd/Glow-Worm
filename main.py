import os
from flask import Flask, request, json, jsonify, make_response
from slackclient import SlackClient

VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
USER_TOKEN = os.environ.get("USER_TOKEN")

app = Flask(__name__)

sc = SlackClient(BOT_TOKEN)
sc_user = SlackClient(USER_TOKEN)


def reaction_parser(channel_id, ts, user_id):
    payload = sc.api_call("reactions.get", channel=channel_id,
                          timestamp=ts)

    if payload["ok"] == True:
        print("parsing reactions")  # debug
        link = payload["message"]["permalink"]
        message = "Here are the reactions for: " + link + " \n"
        attachment_list = []
        reactions = payload["message"]["reactions"]
        # looping through reactions to build our list
        # each reaction has its list of users and will be a separate line
        for index, reaction in enumerate(reactions):
            emoji = ":{}:".format(reaction["name"])
            user_ids = []
            for reacting_user_id in reaction["users"]:
                user_ids.append("<@{}>".format(reacting_user_id))
            users = ", ".join(user_ids)
            attachment = {
                "title": "%s (%s)" % (emoji, str(reaction["count"])),
                "text": users,
                "color": "#2eb886",
                "callback_id": "interactive_message",
                "actions": [
                    {
                        "name": "email_"+str(index),
                        "text": "Get emails",
                        "type": "button",
                        "value": "email"
                    },
                    {
                        "name": "invite_"+str(index),
                        "text": "invite to conversation",
                        "type": "select",
                        "data_source": "conversations"
                    }
                ]
            }
            attachment_list.append(attachment)
        # posting two separate message in order to trigger the link unfurl
        # first, and then the list of reactions
        sc.api_call("chat.postMessage", text=message,
                    channel=user_id, as_user="true")
        sc.api_call("chat.postMessage",
                    channel=user_id, as_user="true", attachments=attachment_list)
    else:
        # TODO add error Handling
        pass


def pretty_json(json_data):
    """
    easily readable JSON
    stolen from Benoit's app!
    """
    return json.dumps(
        json_data, sort_keys=True, indent=4, separators=(',', ': ')
    )


@app.route("/actions", methods=["POST"])
def actions():
    """
    action endpoint, receiving payloads when user clicks the action
    grabbing the relevant values and parsing the reactions
    """
    payload = json.loads(request.form.get("payload"))
    print(pretty_json(payload))  # debug
    if payload["token"] == VERIFICATION_TOKEN:
        if payload["callback_id"] == "reaction_parse":
            # case: action
            ts = payload["message"]["ts"]
            channel_id = payload["channel"]["id"]
            user_id = payload["user"]["id"]
            reaction_parser(channel_id, ts, user_id)
        elif payload["callback_id"] == "interactive_message":
            # case: button click / menu selection
            # we've stored 2 info in the name: the action (email or invite) and
            # the index of the corresponding attachment
            choice, attachment_index = payload["actions"][0]["name"].split("_")
            users = payload["original_message"]["attachments"][int(
                attachment_index)]["text"]
            # removing the "<@" and ">" from the string listing users
            users = users.replace("<@", "").replace(">", "").replace(" ", "")
            if choice == ("email"):
                print(users)  # debug
                users = users.split(",")
                emails = []
                for user in users:
                    resp = sc_user.api_call(
                        "users.profile.get",
                        user=user
                    )
                    print(pretty_json(resp))  # debug
                    # TODO add error handling
                    emails.append(resp["profile"]["email"])
                response = {
                    "text": "here's the full list of emails: " + ", ".join(emails),
                    "replace_original": False
                }
                return make_response(jsonify(**response), 200)
            elif choice == ("invite"):
                print(users)  # debug
                conversation = payload["actions"][0]["selected_options"][0]["value"]
                # TODO add support for more than 30 users
                resp = sc_user.api_call(
                    "conversations.invite",
                    channel=conversation,
                    users=users
                )
                print(pretty_json(resp))
                response = {
                    "text": "Invited users to <#{}>".format("conversation"),
                    "replace_original": False
                }
                return make_response(jsonify(**response), 200)
        return make_response("OK", 200)
    else:
        return make_response("wrong token, who dis", 403)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, host="0.0.0.0", port=port)
