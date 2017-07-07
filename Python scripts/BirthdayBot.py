import time
import os
from slackclient import SlackClient

#-----------------------------
# I have haphazardly stripped out the "next gen" specific info due to a certain someone's impatience.
# A working update will be posted soon as I have the chance.
#-----------------------------

SLACK_TOKEN = ""

birthday_boy = ''
birthday_list = [{'userid':'', 'day':23, 'month':6}]
slack_client = SlackClient(SLACK_TOKEN)
READ_WEBSOCKET_DELAY = 2

#------------------------------
# This cannot be done by a bot user but I will leave it in for posterity
#
#def invite_jeff(post):
#  if post and 'type' in post:
#    if post['type'] == 'member_left_channel' and post['user'] == '': #Jeff just left a channel
#      api_response = slack_client.api_call(
#        "channels.invite",
#        channel=post['channel'],
#        user=post['user']
#        )
#------------------------------

def set_birthday_boy(birthdays):
  date = time.gmtime()
  for user in birthdays:
    if user['day'] == date.tm_mday and user['month']==date.tm_mon:
      birthday_boy = user['userid']

def annoy_pascal(post):
  if post and 'user' in post and 'text' in post:
    info = slack_client.api_call(
      "users.info",
      user=post['user']
      )['user']
    for word in post['text'].split():
      slack_client.api_call(
        "chat.postMessage",
        channel=post['channel'],
        text=word,
        username=info['name'],
        icon_url=info['profile']['image_original']
        )
    slack_client.api_call(
      "chat.delete",
      channel=post['channel'],
      ts = post['ts']
      )

def react_with_cake(post):
  if post and 'ts' in post and 'channel' in post and 'text' in post:
    slack_client.api_call(
      "reactions.add",
      channel=post['channel'],
      name="birthday",
      timestamp=post['ts']
      )

def parse_rtm(rtm_return):
  if rtm_return and len(rtm_return) > 0:
    for output in rtm_return:
      if output and 'text' in output and birthday_boy in output['user']:
        react_with_cake(output)
      if (output and 
          'text' in output and
          'user' in output and
          'channel' in output and
          '' in output['channel']):
        annoy_pascal(output)

if __name__ == '__main__':
  #RTM Connection
  if slack_client.rtm_connect():
    print("BirthdayBoy has connected and is now running!")
    set_birthday_boy(birthday_list)
    while True:
      try:
        parse_rtm(slack_client.rtm_read())
        time.sleep(READ_WEBSOCKET_DELAY)
      except ConnectionResetError:
        slack_client.rtm_connect()
        print('connection lost, retrying')
        time.sleep(60)
  else:
    print("RTM Connection Failure. Check Token, try again.")