from discord import ButtonStyle, Interaction, ui
import discord
import database

CLUB_BLUE = discord.Color.from_rgb(37, 150, 190)

class ViewButton(ui.Button):
    def __init__(self, url):
        super().__init__(style=ButtonStyle.link, label="View Event", url=url)

class EditButton(ui.Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.primary, label="Edit", emoji="✏️")

    async def callback(self, interaction: Interaction):
        response_message = (
            'You clicked Edit! '
            'Please message <@1176403517288755231> to edit your event.'
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
        view = ui.View(timeout=None)
        view.add_item(CancelDeleteButton())
        view.add_item(ConfirmDeleteButton(self.event_id))
        response_message = (
            '**You clicked Delete!**\n'
            'Are you sure you want to **delete** this event? '
            'If this is an accidental deletion, please click **Cancel**.'
        )
        await interaction.response.send_message(response_message, view=view, ephemeral=True)

        