from discord.ext import commands
from slash_commands.utils import guild_exists, channel_exists
import database

async def unlink(ctx: commands.Context):
    await ctx.respond("Unlinking...", ephemeral=True)
    guild = ctx.guild
    channel = ctx.channel
    if channel_exists(str(channel.id)):
        database.delete_channel(str(channel.id))
        await ctx.respond(f"This channel, <#{channel.id}> is now unlinked from UWClubs. Events posted in this channel will no longer be added to the UWClubs website.", ephemeral=True)
    else:
        await ctx.respond(f"This channel, <#{channel.id}> is not linked to UWClubs.", ephemeral=True)

