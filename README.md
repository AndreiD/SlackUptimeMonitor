# Website Down Notifier on Slack

A simple, one file script that notifies you on slack when your website is down.

<img src="https://raw.githubusercontent.com/AndreiD/SlackUptimeMonitor/master/slackmonitor.JPG" alt="slack website up down notifier uptime ping"/>

# Configuration

### Step 1 - Setup the config variables.

URLS_TO_CHECK = ["http://facebook.com",
                 "https://youtube.com:9540"]

### Step 2 -  Getting the Token

#### You have to have a token so you can send messages to a slack channel!
https://api.slack.com/docs/oauth-test-tokens

You need then to export it as an environmental variable or hardcoded

~~~~
export SLACK_TOKEN = 'your_token_here'
~~~~

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

#### Where you want to receive your notifications ?

you can get it using list_channels and channel_info or click on the channel name

click on add app or integration and you can view it's id in the webpage redirection (you have to be fast because it redirects it to another page)

~~~~
CHANNEL_ID = "G2LCBCXGF"
~~~~


### Step 3 - ???

### Step 4 - Profit

### Remember to star this repository and fork it.

#### Bugs / Issues / Suggestions -> write me a message on "Issues"


