from discord import Message, TextChannel, Guild
from supabase import create_client, Client
from consts.secrets import SUPABASE_URL, SUPABASE_KEY
from utils import create_shortname, create_secret

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

def get_all_events_description_and_message_id():
    response = supabase.table("events").select("description"," message_id").execute()

    if response.get('error') is not None:
        raise Exception(f"Supabase API error: {response['error']}")
    
    data = response.data

    eventTuples = [(row['description'], (row['message_id'])) for row in data]

    return eventTuples

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

def create_edit_event_form(event_id: str):
    form_data = {
        "action": "edit",
        "item": "event",
        "item_id": event_id,
    }
    
    # if form already exists, just renew expiry time
    existing_form = supabase.table("forms").select("*").eq("item_id", form_data["item_id"]).eq("item", form_data["item"]).eq("action", form_data["action"]).execute()
    if existing_form.data:
        existing_form_id = existing_form.data[0]["id"]
        response = supabase.table("forms").update({"updated_at": "now()"}).eq("id", existing_form_id).execute()
        return response
    
    # otherwise create a new form
    form_data["secret"] = create_secret()
    response = supabase.table("forms").insert(form_data).execute()
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
