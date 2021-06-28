from discord.utils import get
import imagehash
import discord
import io
from discord.ext import commands
import psycopg2
import PIL.Image as Image
from psycopg2 import errorcodes
import re
import os

db_password = os.environ["DB_PASS"]
bot_token = os.environ["BOT_TOKEN"]
bot = commands.Bot(command_prefix='>')

conn = psycopg2.connect('dbname=postgres user=postgres password={db_password}')
cur = conn.cursor()

@bot.event
async def on_message(message): 
    print("Message", message)
    if(is_message_url(message.content.lower())):
        await process_hyperlink_message(message)

    if(len(message.attachments) > 0): 
        await process_discord_attachment(message)

def is_message_url(message): 
    return bool(re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message))

async def process_hyperlink_message(message):
        try: 
            cur.execute("INSERT INTO images (links) VALUES(%s)", (message.content.lower(), ))
            conn.commit()
        except Exception as e: 
            conn.rollback()
            if(errorcodes.lookup(e.pgcode) == "UNIQUE_VIOLATION"): 
                await message.reply('''```
            ▀█▀ █░█ █ █▀   █ █▀   ▄▀█   █▀█ █▀▀ █▀█ █▀█ █▀ ▀█▀ █   
            ░█░ █▀█ █ ▄█   █ ▄█   █▀█   █▀▄ ██▄ █▀▀ █▄█ ▄█ ░█░ ▄   
            
            █▀█ █ █▀▀ █░█ ▀█▀   ▀█▀ █▀█   ░░█ ▄▀█ █ █░░ █
            █▀▄ █ █▄█ █▀█ ░█░   ░█░ █▄█   █▄█ █▀█ █ █▄▄ ▄                                                                                                                                                                                                                                                                                                                                                                                                                                
  ```''')

async def process_discord_attachment(message):
    for images in message.attachments: 
            # cur = conn.cursor()
            content = await images.read()
            image = Image.open(io.BytesIO(content))
            hashed_discord_image = str(imagehash.average_hash(image))
            # print("Type of Global Var: ", type(hashed_discord_image), hashed_discord_image)
            try: 
                cur.execute("INSERT INTO images (image_hash) VALUES(%s)", (hashed_discord_image, ))
                conn.commit()
                print("Yeah! We stored it!")
            except Exception as e: 
                conn.rollback()
                print("There was an Exception!", e)
                if(errorcodes.lookup(e.pgcode) == "UNIQUE_VIOLATION"): 
                    print("something")
                    await message.reply('''```
            ▀█▀ █░█ █ █▀   █ █▀   ▄▀█   █▀█ █▀▀ █▀█ █▀█ █▀ ▀█▀ █   
            ░█░ █▀█ █ ▄█   █ ▄█   █▀█   █▀▄ ██▄ █▀▀ █▄█ ▄█ ░█░ ▄   
            
            █▀█ █ █▀▀ █░█ ▀█▀   ▀█▀ █▀█   ░░█ ▄▀█ █ █░░ █
            █▀▄ █ █▄█ █▀█ ░█░   ░█░ █▄█   █▄█ █▀█ █ █▄▄ ▄                                                                                                                                                                                                                                                                                                                                                                                                                               
  ```''')


@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)

def client():
    print ('hello world')
    async def on_message(ctx): 
        await ctx.send('pong')
    on_message()

bot.run(bot_token)
