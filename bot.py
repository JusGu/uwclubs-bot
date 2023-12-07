import ai_parser
import discord
from dotenv import load_dotenv
from event import is_event, get_event
from event_error import is_event_error, get_event_error
import os
import database

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

allowed_channels = [1182195509297958952]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.channel.id in allowed_channels:
            parsed_message = ai_parser.parse_message(message.content)
            if is_event(parsed_message):
                event = get_event(parsed_message)
                response = database.insert_event(event)
                print(response)
            elif is_event_error(parsed_message):
                event_error = get_event_error(parsed_message)
                response = database.insert_event_error(event_error)
                print(response)
            else:
                raise Exception("Message is neither an event nor an event error.")

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(TOKEN)

if __name__ == "__main__":
    run_bot()