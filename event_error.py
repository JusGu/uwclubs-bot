import json

class Event_Error:
    def __init__(self, original_message: str, reason_for_error: str):
        self.original_message = original_message
        self.reason_for_error = reason_for_error

def is_event_error(parsed_message: json) -> bool:
    return parsed_message["status"] == "error" or parsed_message["status"] == "unparseable"

def get_event_error(parsed_message: json) -> Event_Error:
    if is_event_error(parsed_message):
        return Event_Error(
            parsed_message["original_message"],
            parsed_message["data"]["reason_for_error"]
        )
    else:
        raise Exception("Message is not an event error.")
    