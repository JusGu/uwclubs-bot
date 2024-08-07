import json
from dateutil import parser
from datetime import datetime

class Event:
    def __init__(self, title: str, start_time: datetime, end_time: datetime, description: str, location: str, recurring: str):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location
        self.recurring = recurring

def is_event(parsed_message: json) -> bool:
    return parsed_message["status"] == "success"

def get_event(parsed_message: json) -> Event:
    if is_event(parsed_message):
        start_time = parser.parse(parsed_message["data"]["start_time"])
        end_time = parser.parse(parsed_message["data"]["end_time"]) if parsed_message["data"]["end_time"] else None
        return Event(
            parsed_message["data"]["title"],
            start_time,
            end_time,
            parsed_message["data"]["description"],
            parsed_message["data"]["location"],
            parsed_message["data"]["recurring"]
        )
    else:
        raise Exception("Message is not an event.")
    
