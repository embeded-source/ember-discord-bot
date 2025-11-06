import discord
from discord.ext import commands
import google.generativeai as genai
import os

# Токены
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Настройка Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} запущен и готов к работе (Gemini активен).")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "ember":
        try:
            prompt = f"Ты — личный ассистент John Leslow по имени Ember. Ответь на сообщение: {message.content}"
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Ошибка при запросе к Gemini: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
