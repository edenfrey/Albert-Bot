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
        print(f'Message from {message.author}: {message.content}')
         # don't respond to ourselves
        if message.author == self.user:
            return
        elif self.user.mentioned_in(message):
            answer = self.chatGPT(message.content[23:])
            await message.channel.send(answer)
        else:
            return        

    def chatGPT(self, query):
        completion = CGPT.Completion.create(
        engine=CGPT_MODEL,
        prompt=query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
        response = completion.choices[0].text
        return response


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(BOT_TOKEN)