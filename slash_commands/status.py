from discord.ext import commands
import database
from datetime import datetime, timezone

async def status(ctx: commands.Context):
    linked_channels = database.select_channel_by_guild_id(str(ctx.guild.id))
    channel_count = len(linked_channels.data)

    if channel_count == 0:
        await ctx.respond(f"## No channels linked.\n\nUse `/link` to link a channel to UWClubs.", ephemeral=True)
    else:
        formatted_channels = []
        for channel in linked_channels.data:
            days_ago = int((datetime.now(timezone.utc) - datetime.fromisoformat(channel['created_at'])).total_seconds() / 86400)
            if days_ago == 0:
                days_ago_str = "today"
            else:
                days_ago_str = f"{days_ago} days ago"
            formatted_channels.append(f"### <#{channel['channel_id']}> (linked {days_ago_str})")
        formatted_channels_str = "\n".join(formatted_channels)
        await ctx.respond(f"{channel_count} linked {'channel' if channel_count == 1 else 'channels'} in {ctx.guild.name}:\n{formatted_channels_str}", ephemeral=True)
