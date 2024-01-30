import ai_parser
from event import is_event, get_event
from event_error import is_event_error, get_event_error
import database
import discord

async def handle_message(self, message: discord.Message):
    await message.add_reaction("🔄")
    parsed_message = ai_parser.parse_message(message.content)
    if is_event(parsed_message):
        event = get_event(parsed_message)
        response = database.insert_event(event, message)
        print(response)
        await message.author.send(f'Your event has been successfully inserted. You can view it at https://www.uwclubs.com/events/{message.id}', view=MyView())
    elif is_event_error(parsed_message):
        event_error = get_event_error(parsed_message)
        response = database.insert_event_error(event_error, message)
        print(response)
    else:
        raise Exception("Message is neither an event nor an event error.")
    await message.remove_reaction("🔄", self.user)
