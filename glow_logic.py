from slackclient import SlackClient
import os

import main


def user_iteration(member_list):
    members = member_list['members']
    print(members)
    for target, next_target in zip(members, members[1:]):
        """
        ignores certain users to avoid Dm'ing. 
        UB43F512L is the bot
        U938A515W is specious
        This can be replaced with a while loop or 
        exclusion through an if in block
        """

        if target == "UB43F512L":
            print(f"skipping {target}")
        else:

            main.sc.api_call("chat.postMessage", channel=target,
                             text=f"hey <@{target}>! here we glow! Say " +
                             f"something nice about <@{next_target}>!",
                             as_user="true")
