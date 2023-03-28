import discord
import os
import logging
import openai
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# create logger
def init_logging(logger):
    # logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    handler_rot_file = RotatingFileHandler(filename='discord-bot.log', encoding='utf-8', mode='a')
    handler_rot_file.setLevel(logging.DEBUG)
    handler_rot_file.setFormatter(log_formatter)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.DEBUG)
    handler_console.setFormatter(log_formatter)

    logger.addHandler(handler_rot_file)
    logger.addHandler(handler_console)

    return logger

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
        
            if message.content == 'ping':
                await message.channel.send('pong')
                logger.info('pong')
            elif classify_intent(message.content) == 'cheap':
                await message.channel.send('cheap')
                logger.info('pong')
            elif classify_intent(message.content) == 'expensive':
                await message.channel.send('expensive')
                logger.info('expensive')
            else:
                await message.channel.send('???')
                logger.info('???')
                

def classify_intent(prompt):
    model_engine = "text-davinci-002"  # or any other OpenAI model that suits your use case

    # define the prompt to use for classification
    prompt = (f"Please classify the following user input into one of the following categories: "
              f"1. cheap\n2. expensive\n\n"
              f"User Input: {prompt}\nCategory:")

    # send prompt to OpenAI's API for classification
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # retrieve the predicted intent code from the response
    predicted_intent = response.choices[0].text.strip().lower()

    # return the predicted intent code
    return predicted_intent


        

if __name__ == "__main__":
    load_dotenv()

    logger = init_logging(logging.root)
    openai.api_key = (os.getenv('OPENAI_KEY'))


    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    client.run(os.getenv('DISCORD_BOT_TOKEN'))