import os
from api import main
from slackclient import SlackClient
from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def user_iteration(member_list):
    b_token = os.environ.get('GLOW_BOT_TOKEN')

    sc = SlackClient(b_token)

    members = member_list['members']
    check_list = list(members)
    check_list.remove("UB43F512L")
    """
    ignores certain users to avoid Dm'ing. 
    UB43F512L is the bot
    U938A515W is specious
    """

    for target in check_list:

        user_target_list = list(check_list)
        user_target_list.remove(target)

        for user in user_target_list:

            sc.api_call("chat.postMessage", channel=target,
                        text=f"hey <@{target}>! here we glow! Say " +
                        f"something nice about <@{user}>!",
                        as_user="true")
