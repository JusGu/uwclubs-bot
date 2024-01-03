import ai_parser
import discord
from discord.ext import commands
from event import is_event, get_event
from event_error import is_event_error, get_event_error
import database
from consts.secrets import DISCORD_BOT_TOKEN, DISCORD_BOT_ID
from slash_commands.link import link
from slash_commands.unlink import unlink
from slash_commands.help import help
from slash_commands.utils import channel_exists

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

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        print(message.author.id)
        if message.author.id != DISCORD_BOT_ID and channel_exists(str(message.channel.id)):
            parsed_message = ai_parser.parse_message(message.content)
            if is_event(parsed_message):
                event = get_event(parsed_message)
                response = database.insert_event(event)
                print(response)
            elif is_event_error(parsed_message):
                event_error = get_event_error(parsed_message)
                response = database.insert_event_error(event_error)
                print(response)
            else:
                raise Exception("Message is neither an event nor an event error.")

def get_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = MyBot(intents=intents)
    return bot

if __name__ == "__main__":
    bot = get_bot()
    bot.run(DISCORD_BOT_TOKEN)