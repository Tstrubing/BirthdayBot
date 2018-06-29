import time

#--------------------------
#  Travis's scripts
#  Written mostly by Travis with aid of Joe D.
#  If this ever becomes more formal I will come up with a better setup 
#    than this but meh it works for now
#--------------------------

def set_birthday_boy(birthdays):
  date = time.gmtime()
  list = []
  for user in birthdays:
    if user['day'] == date.tm_mday and user['month']==date.tm_mon:
      list.append(user['userid'])
  if list
    return list
  else
    return NULL

def react_with_cake(post):   #flag = cake
  if post and 'ts' in post and 'channel' in post and 'text' in post:
    slack_client.api_call(
      "reactions.add",
      channel=post['channel'],
      name="birthday",
      timestamp=post['ts']
      )

def single_word_posts(post):   #flag = singles
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

#------------------------------
# This cannot be done by a bot user but I will leave it in for posterity
#
#def reinvite_user(post):
#  if post and 'type' in post:
#    if post['type'] == 'member_left_channel' and post['user'] == '': #user just left a channel
#      api_response = slack_client.api_call(
#        "channels.invite",
#        channel=post['channel'],
#        user=post['user']
#        )
#------------------------------