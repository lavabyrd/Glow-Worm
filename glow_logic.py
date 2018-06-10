from slackclient import SlackClient
import os

import main


def user_iteration(member_list):
    for i in member_list['members']:
        """
        ignores certain users to avoid Dm'ing. 
        UB43F512L is the bot
        U938A515W is specious
        This can be replaced with a while loop or 
        exclusion through an if in block
        """

        if i == "UB43F512L":
            print(f"skipping {i}")
        else:
            main.sc.api_call("chat.postMessage", channel=i,
                             text=f"hey <@{i}>! here we glow!", as_user="true")
