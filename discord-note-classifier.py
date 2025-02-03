import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class CoursesButtons(discord.ui.View):
    def __init__(self, courses, *, timeout=180):
        super().__init__(timeout=timeout)
        for course in courses:
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, label=course, custom_id=f'button_{course}'))
    
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary)
    async def on_button_click(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(f'You clicked {button.label}', ephemeral=True)

@client.event
async def on_ready():
    print(f"已成功載入 NotesClassifier")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '筆記上傳' not in message.channel.name: 
        return
    
    await message.add_reaction('📚')
    guild = message.guild
    categories = [category for category in guild.categories]
    courses = []
    for category in categories:
        for channel in category.channels:
            if '筆記' in channel.name:
                courses.append(category.name)
    await message.channel.send("Please select a course:", view=CoursesButtons(courses))
    print(courses)

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token)