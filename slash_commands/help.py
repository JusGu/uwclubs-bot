from discord.ext import commands

async def help(ctx: commands.Context):
    help_message = (
        "`/help`: View this message.\n"
        "`/link`: Link this Discord channel to UWClubs. Requires admin privileges.\n"
        "`/unlink`: Unlink this Discord channel from UWClubs. Requires admin privileges."
    )
    await ctx.respond(help_message, ephemeral=True)