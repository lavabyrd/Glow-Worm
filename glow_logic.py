from slackclient import SlackClient
import os

import main

from flask import Flask

from tasks import make_celery
app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


@celery.task
def user_iteration(member_list):
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

            main.sc.api_call("chat.postMessage", channel=target,
                             text=f"hey <@{target}>! here we glow! Say " +
                             f"something nice about <@{user}>!",
                             as_user="true")
