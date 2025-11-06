import discord
from discord.ext import commands
import google.generativeai as genai
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
    # Проверяем, что сообщение не от бота
    if message.author == bot.user:
        return

    # Реагируем только в нужном канале
    if message.channel.name == "ember":
        try:
            response = model.generate_content(message.content)
            reply = response.text.strip()

            # Отправляем только один ответ
            if reply:
                await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"Ошибка при запросе к Gemini: {e}")

    # Обязательно пропускаем командные сообщения
    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
