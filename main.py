import discord
from discord.ext import commands
import openai
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} запущен и готов к работе.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "ember":
        from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

...

if message.channel.name == "ember":
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты — личный ассистент John Leslow по имени Ember."},
            {"role": "user", "content": message.content}
        ]
    )
    await message.channel.send(response.choices[0].message.content)


    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
