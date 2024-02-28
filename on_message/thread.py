import discord
from discord import ui
from consts.get_env import get_link
from on_message.shared.embed import create_event_embed
from on_message.shared.view import ViewButton
from event import Event

async def create_confirmation_thread(event: Event, message: discord.Message):
    thread = await message.create_thread(name=event.title, auto_archive_duration=60)
    view = ui.View()
    view.add_item(ViewButton(f"{get_link()}events/{message.id}"))
    text = "Your event has been successfully created."
    embed = create_event_embed(event, message)

    await thread.send(text, view=view, embed=embed)
