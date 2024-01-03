from discord.ext import commands

async def unlink(ctx: commands.Context):
    await ctx.respond("unlinked!", ephemeral=True)
