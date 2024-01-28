import database

def channel_exists(channel_id: str):
    channel_response = database.select_channel_by_channel_id(channel_id).model_dump(mode="json")
    return len(channel_response['data']) > 0

def guild_exists(guild_id: str):
    guild_response = database.select_guild(guild_id).model_dump(mode="json")
    print(guild_response)
    return len(guild_response['data']) > 0