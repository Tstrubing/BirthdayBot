import time
import os
from slackclient import SlackClient
from travisscripts import *

#-----------------------------
# Current version: BBot V0.5
# Released: 7/19/2017
# Written by: Travis Strubing
#   with help from: Joey Domino
#-----------------------------

birthday_boy = ''
birthday_list = []   #will be an array of dicts of format[{'userid':'', 'day':#, 'month'#6}]
active_flags = []    #Array of Dicts format: [{'userid':'', 'flags':['flag1','flag2']}]
SLACK_TOKEN = ''
READ_WEBSOCKET_DELAY = 0

def parse_rtm(rtm_return):
  if rtm_return and len(rtm_return) > 0:
    for output in rtm_return:
      if output and 'user' in output:
        for userflag in active_flags:
          if 'userid' in userflag == 'user' in output
            if 'text' in output and 'cake' in userflag['flags']:
              react_with_cake(output)
            if 'text' in output and 'channel' in output and ''singles' in userflag['flags']:
              single_word_posts(output)

def get_settings():
  flags = FALSE
  birthdays = FALSE
  global birthday_list, active_flags, SLACK_TOKEN, READ_WEBSOCKET_DELAY
  with open('settings.txt','r+') as settings:
    settings.read() #purge the explination line
    for entry in settings:
      if entry == 'token':
        SLACK_TOKEN = settings.read()[2:]
        print SLACK_TOKEN
      if entry == 'web_delay':
        READ_WEBSOCKET_DELAY = settings.read()[2:]
        print READ_WEBSOCKET_DELAY
      if entry == 'flags':
        flags = TRUE

      
        active_flags.append({'userid':

if __name__ == '__main__':
  #setup variables
  get_settings()
  slack_client = SlackClient(SLACK_TOKEN) #real token found in settings file
  #RTM Connection
  if slack_client.rtm_connect():
    print("BirthdayBoy has connected and is now running!")
    birthday_boy = set_birthday_boy(birthday_list)
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