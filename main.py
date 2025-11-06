import discord
from discord.ext import commands
import google.generativeai as genai
import os

# Настройки токенов
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_KEY)

# Настройки Discord
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
        try:
            # Используем актуальную модель Gemini
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(message.content)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Ошибка при запросе к Gemini: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
