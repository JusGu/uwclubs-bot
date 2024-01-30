from discord.ext import commands
import database
from slash_commands.utils import guild_exists, channel_is_linked

async def link(ctx: commands.Context):
    await ctx.respond("Linking...", ephemeral=True)
    guild = ctx.guild
    channel = ctx.channel
    if not guild_exists(str(guild.id)):
        database.insert_guild(guild)
        database.insert_channel(channel)
        await ctx.respond(f"Welcome to UWClubs! This channel, <#{channel.id}> is now linked to UWClubs. All events posted in this channel will be added to the UWClubs website.", ephemeral=True)
    elif not channel_is_linked(str(channel.id)):
        database.insert_channel(channel)
        await ctx.respond(f"This channel, <#{channel.id}> is now linked to UWClubs. All events posted in this channel will be added to the UWClubs website.", ephemeral=True)
    else:
        await ctx.respond(f"This channel, <#{channel.id}> is already linked to UWClubs.", ephemeral=True)
