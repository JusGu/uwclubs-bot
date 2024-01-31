from discord import ButtonStyle, Interaction, ui
import database

class ViewButton(ui.Button):
    def __init__(self, url):
        super().__init__(style=ButtonStyle.link, label="View", url=url)

class EditButton(ui.Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.primary, label="Edit", emoji="✏️")

    async def callback(self, interaction: Interaction):
        response_message = (
            'You clicked Edit! '
            'Please message me to edit your event.'
        )
        await interaction.response.send_message(response_message)

class ConfirmDeleteButton(ui.Button):
    def __init__(self, event_id):
        super().__init__(style=ButtonStyle.danger, label="Confirm Delete")
        self.event_id = event_id

    async def callback(self, interaction: Interaction):
        database.delete_event(self.event_id)
        await interaction.response.send_message("Event successfully deleted.", ephemeral=True)

class CancelDeleteButton(ui.Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.secondary, label="Cancel")

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("Event deletion cancelled.", ephemeral=True)

class DeleteButton(ui.Button):
    def __init__(self, event_id):
        super().__init__(style=ButtonStyle.danger, label="Delete")
        self.event_id = event_id

    async def callback(self, interaction: Interaction):
        view = ui.View()
        view.add_item(CancelDeleteButton())
        view.add_item(ConfirmDeleteButton(self.event_id))
        response_message = (
            '**You clicked Delete!**\n'
            'Are you sure you want to **delete** this event? '
            'If this is an accidental deletion, please click **Cancel**.'
        )
        await interaction.response.send_message(response_message, view=view, ephemeral=True)

async def send_confirmation_message(author, message_id):
    view = ui.View()
    view.add_item(ViewButton(f"https://www.uwclubs.com/events/{message_id}"))
    view.add_item(EditButton())
    view.add_item(DeleteButton(message_id))

    confirmation_message = (
        f"**Hello {author.name},**\n\n"
        "Your event has been successfully inserted. "
        "You can manage your event using the buttons below.\n\n"
        f"**Event Link:** [Click Here](https://www.uwclubs.com/events/{message_id})"
    )

    await author.send(content=confirmation_message, view=view)