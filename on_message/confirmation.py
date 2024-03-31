from discord import ui, Message
from consts.get_env import get_event_link
from on_message.shared.embed import create_event_embed
from on_message.shared.view import DeleteButton, EditButton, ViewButton
from event import Event

        
async def send_confirmation_message(event: Event, message: Message):
    view = ui.View(timeout=None)
    view.add_item(ViewButton(get_event_link(message.id)))
    view.add_item(EditButton(message.id))
    view.add_item(DeleteButton(message.id))

    confirmation_message = (
        f"**Hello {message.author.name},**\n\n"
        "Your event has been successfully added. "
        "You can manage your event using the buttons below.\n\n"
    )
    embed = create_event_embed(event, message)

    await message.author.send(content=confirmation_message, view=view, embed=embed)

async def send_edit_confirmation_message(author, message_id):
    view = ui.View(timeout=None)
    view.add_item(ViewButton(f"{get_event_link(message_id)}"))
    view.add_item(EditButton())
    view.add_item(DeleteButton(message_id))

    confirmation_message = (
        f"**Hello {author.name},**\n\n"
        "Your event has been successfully edited. "
        "You can manage your event using the buttons below.\n\n"
        f"**Event Link:** [Click Here]({get_event_link(message_id)})\n\n"
    )

    await author.send(content=confirmation_message, view=view)
