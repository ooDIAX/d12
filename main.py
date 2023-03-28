import discord
import os
import logging
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

        if message.content == 'ping':
            await message.channel.send('pong')
            logger.info('pong')

        

if __name__ == "__main__":
    logger = init_logging(logging.root)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    load_dotenv()
    client.run(os.getenv('TOKEN'))