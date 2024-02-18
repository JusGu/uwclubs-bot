from discord import Message, TextChannel, Guild
from supabase import create_client, Client
from consts.secrets import SUPABASE_URL, SUPABASE_KEY
from utils import create_shortname

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_event(event, message: Message):
    event_data = {
        "title": event.title,
        "start_time": event.start_time.isoformat(),
        "description": event.description,
        "location": event.location,
        "recurring": event.recurring,
        "message_id": str(message.id),
        "channel_id": str(message.channel.id),
        "guild_id": str(message.guild.id),
    }
    if event.end_time:
        event_data["end_time"] = event.end_time.isoformat()
        
    response = supabase.table("events").insert(event_data).execute()
    return response

def insert_event_error(event_error, message: Message):
    event_error_data = {
        "original_message": event_error.original_message,
        "reason_for_error": event_error.reason_for_error,
        "message_id": str(message.id),
        "channel_id": str(message.channel.id),
        "guild_id": str(message.guild.id),
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
        "full_name": guild.name,
        "short_name": create_shortname(guild.name),
        "description": guild.description
    }
    response = supabase.table("guilds").insert(guild_data).execute()
    return response

def edit_event(event: str, message: Message):
    event_data = {
        "title": event.title,
        "start_time": event.start_time.isoformat(),
        "description": event.description,
        "location": event.location,
    }
    if event.end_time:
        event_data["end_time"] = event.end_time.isoformat()
    response = supabase.table("events").update(event_data).eq("message_id", message.id).execute()
    return response



def select_channel_by_channel_id(channel_id: str):
    response = supabase.table("channels").select("*").eq("channel_id", channel_id).is_("deleted_at", "NULL").execute()
    return response

def select_channel_by_guild_id(guild_id: str):
    response = supabase.table("channels").select("*").eq("guild_id", guild_id).is_("deleted_at", "NULL").execute()
    return response

def select_channels():
    response = supabase.table("channels").select("*").is_("deleted_at", "NULL").execute()
    return response

def select_guild(guild_id: str):
    response = supabase.table("guilds").select("*").eq("guild_id", guild_id).is_("deleted_at", "NULL").execute()
    return response

def delete_event(event_id: str):
    response = supabase.table("events").update({"deleted_at": "now()"}).eq("message_id", event_id).execute()
    return response

def delete_channel(channel_id: str):
    response = supabase.table("channels").update({"deleted_at": "now()", "updated_at": "now()"}).eq("channel_id", channel_id).execute()
    return response



