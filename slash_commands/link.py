from discord.ext import commands
import database

def channel_exists(channel_id: str):
    channel_response = database.select_channel(channel_id).model_dump(mode="json")
    return len(channel_response['data']) > 0

def guild_exists(guild_id: str):
    guild_response = database.select_guild(guild_id).model_dump(mode="json")
    print(guild_response)
    return len(guild_response['data']) > 0

async def link(ctx: commands.Context):
    guild = ctx.guild
    channel = ctx.channel
    print(guild_exists(str(guild.id)))
    if not guild_exists(str(guild.id)):
        database.insert_guild(guild)
        database.insert_channel(channel)
        await ctx.respond(f"Welcome to UWClubs! This channel, <#{channel.id}> is now linked to UWClubs. All events posted in this channel will be added to the UWClubs website.", ephemeral=True)
    elif not channel_exists(str(channel.id)):
        database.insert_channel(channel)
        await ctx.respond(f"This channel, <#{channel.id}> is now linked to UWClubs. All events posted in this channel will be added to the UWClubs website.", ephemeral=True)
    else:
        await ctx.respond("This channel is already linked to UWClubs.", ephemeral=True)
