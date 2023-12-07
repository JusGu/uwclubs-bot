import json

from datetime import datetime

class Event:
    def __init__(self, title: str, start_time: datetime, end_time: datetime, description: str, location: str):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location

def is_event(parsed_message: json) -> bool:
    return parsed_message["status"] == "success"

def get_event(parsed_message: json) -> Event:
    if is_event(parsed_message):
        start_time = datetime.fromisoformat(parsed_message["data"]["start_time"])
        end_time = datetime.fromisoformat(parsed_message["data"]["end_time"])
        return Event(
            parsed_message["data"]["title"],
            start_time,
            end_time,
            parsed_message["data"]["description"],
            parsed_message["data"]["location"]
        )
    else:
        raise Exception("Message is not an event.")
    
