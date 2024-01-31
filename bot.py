import ai_parser
import discord
from discord.ext import commands
from event import is_event, get_event
from event_error import is_event_error, get_event_error
import database
from consts.secrets import DISCORD_BOT_TOKEN
from slash_commands.slash_commands import link, unlink, help, status
from slash_commands.utils import channel_is_linked
from on_message.handler import handle_message

async def execute_admin_command(ctx: commands.Context, callback):
    if ctx.author.guild_permissions.administrator:
        await callback(ctx)
    else:
        await ctx.respond("You need to be an administrator to use this command.", ephemeral=True)
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.slash_command(name="link", description="Links this channel to UWClubs. Requires admin privileges.")
        async def link_command(ctx: commands.Context):
            await execute_admin_command(ctx, link)

        @self.slash_command(name="unlink", description="Unlinks this channel from UWClubs. Requires admin privileges.")
        async def unlink_command(ctx: commands.Context):
            await execute_admin_command(ctx, unlink)
        
        @self.slash_command(name="help", description="View a list of bot commands and what they do.")
        async def help_command(ctx: commands.Context):
            await help(ctx)

        @self.slash_command(name="status", description="View a list of currently linked channels.")
        async def status_command(ctx: commands.Context):
            await status(ctx)

    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if channel_is_linked(str(message.channel.id)):
            await handle_message(self, message)

def get_bot():
    intents = discord.Intents.none()
    intents.messages = True
    intents.message_content = True
    intents.reactions = True
    intents.guilds = True
    bot = MyBot(intents=intents)
    return bot

if __name__ == "__main__":
    bot = get_bot()
    bot.run(DISCORD_BOT_TOKEN)