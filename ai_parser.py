from openai import OpenAI
import mock_data
from consts.secrets import OPENAI_API_KEY
from datetime import datetime
import pytz
import discord

def get_system_content(message: discord.Message) -> str:
    current_date = datetime.now().strftime("%B %d, %Y")
    guild = message.guild.name
    channel = message.channel.name
    system_content = f'''You are a helpful assistant parsing messages on discord. 
    The current day is {current_date}.
    You are in the {channel} channel in the {guild} server.
    Please do your best to guide the user with honest information.
    You are to determine if it is an announcement for an event. Meetings are events. Reminder for deadlines are not events.

    If it is an event, output JSON with the fields: title, start_time, end_time, description, location, and recurring.
    Keep the title short but descriptive. "Meeting" or "Event" are not descriptive.
    start_time and end_time are ISO 8601 strings. Do not convert the time to a different timezone.
    If there is no end time, end_time is null.
    Keep the description exactly as it is.
    Location can be online or in a physical location or null.
    If location is in a physical location, it should be in the format: "Building Name Room Number" without "room" in the middle.
    Determine if or when the event is recurring, and fill in the field as follows:
    recurring can take the values: False, Daily, Weekly, Bi-weekly, Monthly, and Bi-monthly.

    If it is not an event, output JSON with the field: reason_for_error.
    '''
    return system_content


import json

def to_est_tz(iso_string):
    dt_naive = datetime.fromisoformat(iso_string)
    tz_ny = pytz.timezone("America/New_York")
    dt_est = tz_ny.localize(dt_naive)
    return dt_est.strftime('%Y-%m-%d %H:%M:%S%z')

def convert_event_to_est(event: dict) -> dict:
    event["start_time"] = to_est_tz(event["start_time"])
    if event["end_time"]:
        event["end_time"] = to_est_tz(event["end_time"])
    return event

def parse_message(message: discord.Message) -> json:
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": get_system_content(message)},
                {"role": "user", "content": message.content}
            ]
        )
        responseJSON = json.loads(response.choices[0].message.content)
        if "reason_for_error" in responseJSON:
            return {"status": "error", "data": responseJSON, "original_message": message.content}
        else:
            return {"status": "success", "data": convert_event_to_est(responseJSON)}
    except Exception as e:
        return {"status": "unparseable", "data": {"reason_for_error": str(e)}, "original_message": message.content}

    
if __name__ == "__main__":
    parsed_message = parse_message(mock_data.message_2)
    print(json.dumps(parsed_message, indent=4))
