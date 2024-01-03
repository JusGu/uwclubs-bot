from discord import TextChannel, Guild
from supabase import create_client, Client
from consts.secrets import SUPABASE_URL, SUPABASE_KEY
from utils import create_shortname

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_event(event):
    event_data = {
        "title": event.title,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        "description": event.description,
        "location": event.location
    }
    response = supabase.table("events").insert(event_data).execute()
    return response

def insert_event_error(event_error):
    event_error_data = {
        "original_message": event_error.original_message,
        "reason_for_error": event_error.reason_for_error
    }
    response = supabase.table("event_errors").insert(event_error_data).execute()
    return response

def insert_channel(channel: TextChannel):
    channel_data = {
        "channel_id": str(channel.id),
        "guild_id": str(channel.guild.id),
    }
    response = supabase.table("channels").insert(channel_data).execute()
    return response

def insert_guild(guild: Guild):
    guild_data = {
        "guild_id": str(guild.id),
        "fullname": guild.name,
        "shortname": create_shortname(guild.name),
        "description": guild.description
    }
    response = supabase.table("guilds").insert(guild_data).execute()
    return response

def select_channel(channel_id: str):
    response = supabase.table("channels").select("*").eq("channel_id", channel_id).is_("deleted_at", "NULL").execute()
    return response

def select_channels():
    response = supabase.table("channels").select("*").is_("deleted_at", "NULL").execute()
    return response

def select_guild(guild_id: str):
    response = supabase.table("guilds").select("*").eq("guild_id", guild_id).is_("deleted_at", "NULL").execute()
    return response

def delete_channel(channel_id: str):
    response = supabase.table("channels").update({"deleted_at": "now()", "updated_at": "now()"}).eq("channel_id", channel_id).execute()
    return response



