from discord import Embed
import discord

from consts.get_env import get_event_link, get_link
from on_message.shared.view import CLUB_BLUE
from event import Event


def create_event_embed(event: Event, message: discord.Message):
    embed = Embed(
        title=event.title,
        url=f"{get_event_link(message.id, message.guild.id)}",
        color=CLUB_BLUE
    )
    embed.set_author(name="UWClubs")
    embed.set_image(url=f"{get_link()}events/{message.id}/opengraph-image")
    embed.set_footer(text="Your contribution helps students discover exciting club events like yours more easily.")
    return embed
