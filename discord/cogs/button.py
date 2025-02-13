import discord
from discord.ext import commands

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

class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='button')
    async def button_command(self, ctx):
        await ctx.send("This message has buttons!", view=Buttons())

async def setup(bot):
    await bot.add_cog(ButtonCog(bot))