# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from slackclient import SlackClient
import requests
import datetime
import pickle

# ================== CONFIGURATION ==================

URLS_TO_CHECK = ["http://facebook.com",
                 "https://youtube.com:9540"]

# You have to have a token so you can send messages to a slack channel!
# https://api.slack.com/docs/oauth-test-tokens
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

# Where you want to receive your notifications ?

# you can get it using list_channels and channel_info or click on the channel name
# click on add app or integration and you can view it's id in the webpage redirection (you have to be fast because it redirects it to another page)
CHANNEL_ID = "G2LCBCXGF"

# ================== END CONFIGURATION ==================


slack_client = SlackClient(SLACK_TOKEN)


# ================== SLACK FUNCTIONS ==================
def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None


def send_message(channel_id, message):
    response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='UptimeMonitor',
        icon_emoji=':robot_face:'
    )
    if not response['ok']:
        print("Error sending notification to Slack -------> " + response['error'])


# ================== NOTIFY FUNCTIONS ==================
def down_notifier(the_url):
    try:
        old_status_file = pickle.load(open("status.p", "rb"))
    except Exception as ex:
        print("The status.p file was not found. it will be recreated." + str(ex))
        send_message(CHANNEL_ID, ":no_entry: " + the_url + " is down.")
        return

    # in case we just added the url to our database
    if the_url not in old_status_file:
        send_message(CHANNEL_ID, ":no_entry: " + the_url + " is down.")
        return

    # if it's already in the database and last status was up
    if (the_url in old_status_file) and (old_status_file[the_url]['status'] == "up"):
        send_message(CHANNEL_ID, ":no_entry: " + the_url + " is down.")


# if it was previously down, notify that it's back online
def back_online_notifier(the_url):
    try:
        old_status_file = pickle.load(open("status.p", "rb"))
    except Exception as ex:
        print("The status.p file was not found. it will be recreated." + str(ex))
        return

    if (the_url in old_status_file) and (old_status_file[the_url]['status'] == "down"):
        it_was_down_time = old_status_file[the_url]['time']
        current_time = datetime.datetime.now().replace(microsecond=0)
        send_message(CHANNEL_ID, ":herb: " + the_url + " is back online. It was down for " + str(current_time - it_was_down_time))


# --- getting only the head ---
def get_status_code(xurl):
    try:
        response = requests.head(xurl, allow_redirects=False, timeout=3)
        return response.status_code
    except:
        return -1


# ~~~~~~~~~~~~~~~~~~~~~~~~ THE MAIN ~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    # First test if you have the correct token
    # print(slack_client.api_call("auth.test"))

    status_file = {}

    for url in URLS_TO_CHECK:
        if get_status_code(url) != 200:
            down_notifier(url)
            status_file[url] = {'status': "down", 'time': datetime.datetime.now().replace(microsecond=0)}

        else:
            back_online_notifier(url)
            status_file[url] = {'status': "up", 'time': datetime.datetime.now().replace(microsecond=0)}

        pickle.dump(status_file, open("status.p", "wb"))
