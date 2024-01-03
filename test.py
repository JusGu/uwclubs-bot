from slash_commands.link import create_shortname
import database



if __name__ == "__main__":
    guild_id = "1181758130544197732"
    channel_id = "1182195509297958952"
    guild_data = {
        "guild_id": guild_id,
        "fullname": "UWClubs",
        "shortname": create_shortname("UWClubs"),
        "description": "UWClubs is a Discord bot that allows you to post events to the UWClubs website."
    }
    response = database.insert_guild(guild_data)
