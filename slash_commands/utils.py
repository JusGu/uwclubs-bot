import database

def channel_is_linked(channel_id: str):
    channel_response = database.select_channel_by_channel_id(channel_id)
    print(channel_response)
    return len(channel_response.data) > 0

def guild_exists(guild_id: str):
    guild_response = database.select_guild(guild_id)
    print(guild_response)
    return len(guild_response.data) > 0