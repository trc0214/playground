import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        for i in range(5):  # Create 5 buttons
            self.add_item(discord.ui.Button(label=f"Button {i+1}", style=discord.ButtonStyle.gray, custom_id=f"button_{i+1}"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.data['custom_id'].startswith('button_'):
            button_number = interaction.data['custom_id'].split('_')[1]
            await interaction.response.edit_message(content=f"This is an edited button response for Button {button_number}!")
            return True
        return False

@client.command()
async def button(ctx):
    await ctx.send("This message has buttons!", view=Buttons())

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token)