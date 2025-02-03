import discord
from discord.ext import commands
from discord import app_commands

class Course(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"已成功載入 Course")

    async def create_category_with_channels(self, guild, category_name):
        new_category = await guild.create_category(category_name)
        await guild.create_text_channel('📢課程公告', category=new_category)
        await guild.create_text_channel('🗒️筆記', category=new_category)
        await guild.create_text_channel('🤔考試與提問', category=new_category)
        return new_category

    async def delete_category_and_channels(self, category):
        for channel in category.channels:
            await channel.delete()
        await category.delete()

    @app_commands.command(name="add_category", description="Add a new category to the server")
    @app_commands.guild_only()
    async def add_category(self, interaction: discord.Interaction, category_name: str):
        guild = interaction.guild
        existing_category = discord.utils.get(guild.categories, name=category_name)
        
        if existing_category:
            await interaction.response.send_message(f"Category '{category_name}' already exists.", ephemeral=True)
        else:
            await self.create_category_with_channels(guild, category_name)
            await interaction.response.send_message(f"Category '{category_name}' and its channels have been created.", ephemeral=True)

    @app_commands.command(name="delete_category", description="Delete a category from the server")
    @app_commands.guild_only()
    async def delete_category(self, interaction: discord.Interaction, category_name: str):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name=category_name)
        
        if category:
            await self.delete_category_and_channels(category)
            await interaction.response.send_message(f"Category '{category_name}' has been deleted.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Category '{category_name}' does not exist.", ephemeral=True)

    @commands.command()
    async def add_course(self, ctx, course_name: str):
        guild = ctx.guild
        existing_category = discord.utils.get(guild.categories, name=course_name)
        
        if existing_category:
            await ctx.send(f"Category '{course_name}' already exists.")
        else:
            await self.create_category_with_channels(guild, course_name)
            await ctx.send(f"Category '{course_name}' and its channels have been created.")

    @commands.command()
    async def delete_course(self, ctx, course_name: str):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name=course_name)
        
        if category:
            await self.delete_category_and_channels(category)
            await ctx.send(f"Category '{course_name}' has been deleted.")
        else:
            await ctx.send(f"Category '{course_name}' does not exist.")

async def setup(bot):
    await bot.add_cog(Course(bot))