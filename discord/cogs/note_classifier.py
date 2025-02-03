import discord
from discord.ext import commands

class CourseButton(discord.ui.Button):
    def __init__(self, label, message):
        super().__init__(style=discord.ButtonStyle.primary, label=label, custom_id=f'button_{label}')
        self.message = message

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You clicked {self.label}', ephemeral=True)
        for category in interaction.guild.categories:
            if category.name == self.label:
                for channel in category.channels:
                    if '筆記' in channel.name:
                        await channel.send(self.message.content)
                        await self.message.delete()
                        return

class CoursesButtons(discord.ui.View):
    def __init__(self, courses, message, *, timeout=180):
        super().__init__(timeout=timeout)
        for course in courses:
            self.add_item(CourseButton(label=course, message=message))
    
class NotesClassifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"已成功載入 NotesClassifier")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if '筆記上傳' not in message.channel.name: 
            return
        
        await message.add_reaction('📚')
        guild = message.guild
        courses = []
        for category in guild.categories:
            for channel in category.channels:
                if '筆記' in channel.name:
                    courses.append(category.name)
        await message.channel.send("Please select a course:", view=CoursesButtons(courses, message=message))
        
async def setup(bot):
    await bot.add_cog(NotesClassifier(bot))