import discord
from discord.ext import commands

class Buttons(discord.ui.View):
    def __init__(self,):
        super().__init__()
        for i in range(5):  # Create 5 buttons
            self.add_item(discord.ui.Button(label=f"Button {i+1}", style=discord.ButtonStyle.gray, custom_id=f"button_{i+1}"))

    @discord.ui.button(label="Button", style=discord.ButtonStyle.gray)
    async def blurple_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.green
        await interaction.response.edit_message(content="This is an edited button response!", view=self)
        await interaction.followup.send("This is a followup message!")

class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='button')
    async def button_command(self, ctx):
        await ctx.send("This message has buttons!", view=Buttons())

async def setup(bot):
    await bot.add_cog(ButtonCog(bot))