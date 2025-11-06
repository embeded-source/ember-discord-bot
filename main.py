import discord
from discord.ext import commands
import google.generativeai as genai
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

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
            response = model.generate_content(message.content)
            reply = response.text.strip()

            # Разбиваем длинный ответ на части по 2000 символов
            max_length = 2000
            for i in range(0, len(reply), max_length):
                await message.channel.send(reply[i:i + max_length])

        except Exception as e:
            await message.channel.send(f"Ошибка при запросе к Gemini: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
