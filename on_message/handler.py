import ai_parser
from event import is_event, get_event
from event_error import is_event_error, get_event_error
import database
import discord
from on_message.confirmation import send_confirmation_message
from on_message.confirmation import send_edit_confirmation_message

async def handle_message(self, message: discord.Message):
    await message.add_reaction("🔄")
    parsed_message = ai_parser.parse_message(message.content)
    if is_event(parsed_message):
        event = get_event(parsed_message)
        response = database.insert_event(event, message)
        print(response)
        await send_confirmation_message(message.author, message.id)
    elif is_event_error(parsed_message):
        event_error = get_event_error(parsed_message)
        response = database.insert_event_error(event_error, message)
        print(response)
    else:
        raise Exception("Message is neither an event nor an event error.")
    await message.remove_reaction("🔄", self.user)

async def handle_message_edit(self, before: discord.Message, after: discord.Message):
    await after.add_reaction("🔄")
    parsed_message = ai_parser.parse_message(after.content)
    if is_event(parsed_message):
        event = get_event(parsed_message)
        response = database.edit_event(event, after)
        print(response)
        await send_edit_confirmation_message(after.author, after.id)
    elif is_event_error(parsed_message):
        event_error = get_event_error(parsed_message)
        response = database.insert_event_error(event_error, after)
        print(response)
    else:
        raise Exception("Message is neither an event nor an event error.")
    await after.remove_reaction("🔄", self.user)