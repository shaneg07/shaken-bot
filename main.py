import os
import discord
import requests
import json
import random
from replit import db

my_secret = os.environ['token'] #hiding the token of my discord bot.
client = discord.Client()

sad_words = ["sad", "depressed", "miserable", "unhappy", "angry", "jealous", "cry", "crying", "hopeless", "the big sad"]
starter_encouragements = ["Hang in there", "You are a beautiful person/bot", "You are a valuable memeber of the society."]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encourage(enc_msg):
  if "encouragements" in db.keys(): 
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_msg]


def delete_encourage(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:

    return

  msg = message.content
  
  if msg.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  if "encouragements" in db.keys():
    options += db["encouragements"]
  
  if msg.startswith("$new"):
    enc_msg = msg.split("$new ", 1)[1]
    update_encourage(enc_msg)
    await message.channel.send("New encouragement added.")
  
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encourage(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$show"):
    encouragements = db["encouragements"]
    await message.channel.send(encouragements)



  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

client.run(my_secret)
