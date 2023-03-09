import discord
import os
from dotenv import load_dotenv
import openai as CGPT

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CGPT_KEY = os.getenv("CHATGPT_KEY")
CGPT_MODEL = "text-davinci-003"
CGPT.api_key = CGPT_KEY

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
         # Don't respond to ourselves
        if message.author == self.user:
            return
        elif not message.guild or self.user.mentioned_in(message): # Anser DMs without @ the bot or answer in guilds if @ the bot.

            # Get past 10 messages of the chat and create messages list.
            messages = [message async for message in message.channel.history(limit=10)]
            context = []
            for msg in messages:
                if msg.author == self.user:
                    context.insert(0,{"role": "assistant", "content": msg.content})
                else:
                    context.insert(0,{"role": "user", "content": msg.content})

            # Call API, get answer, provide answer.
            answer = self.chatGPT(context)
            await message.channel.send(answer)
        else:
            return        

    def chatGPT(self, context):
        response = CGPT.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=context,
          temperature=1.5
        )
        return response.choices[0].message.content


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(BOT_TOKEN)