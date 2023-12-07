from supabase import create_client, Client
from consts.tokens import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_event(event):
    event_data = {
        "title": event.title,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        "description": event.description,
        "location": event.location
    }
    data = supabase.table("events").insert(event_data).execute()
    return data

def insert_event_error(event_error):
    event_error_data = {
        "original_message": event_error.original_message,
        "reason_for_error": event_error.reason_for_error
    }
    data = supabase.table("event_errors").insert(event_error_data).execute()
    return data

