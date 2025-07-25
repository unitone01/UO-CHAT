import discord
import os
import cohere
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
#ALLOWED_CHANNEL = os.getenv("ALLOWED_CHANNEL")

# Setup Cohere
co = cohere.Client(COHERE_API_KEY)

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Keep-alive Flask server
app = Flask('')

@app.route('/')
def home():
    return "UØ-CHAT is running 👾"

def run():
    app.run(host='0.0.0.0', port=8080)

# Start Flask server in background thread
Thread(target=run).start()

@client.event
async def on_ready():
    print(f"🤖 UØ-CHAT is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.name != ALLOWED_CHANNEL:
        return

    prompt = f"""Reply like a chill, human Discord user. No paragraphs. 
Be funny, casual, and short. Reply to:
"{message.content}"
"""

    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=80,
            temperature=0.7
        )
        reply = response.generations[0].text.strip()
        await message.channel.send(reply)
    except Exception as e:
        print("Cohere Error:", e)
        await message.channel.send("Bruh... error aa gaya 😵")

# Start the bot
client.run(DISCORD_TOKEN)
