import os
import discord
import asyncio 
import subprocess
import configparser
import inspect
import textwrap
from datetime import datetime
from contextlib import redirect_stdout
import io
import traceback
from subprocess import Popen
from discord.ext import commands
from discord import ActivityType

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot:commands.Bot = bot
        self._last_result = None 
        
    @commands.command()
    async def ping(self, ctx):
        """Pings to see if it's still alive."""
        await ctx.send("Pika, Pika!! I'm still here!")
    
    @commands.command(aliases=["info"])
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, ctx, *, user: str = None):
        """Looks up information for the user."""
        #TODO: Fix the issue where the bot doesn't info users that are not in the server.
        if user == None:
            user = ctx.author
            member = ctx.guild.get_member(user.id)
        if user != ctx.author:
            try:
                member = await commands.MemberConverter().convert(ctx, user)
                user = member
            except:
                user = await ctx.bot.get_user_info(int(user))
                member = None
        embed = discord.Embed(color=0x7289DA)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        status = str(user.status)
        if user.status == discord.Status.offline:
            status = "Offline"
        elif user.status == discord.Status.dnd:
            status = "Do Not Disturb"
        elif user.status == discord.Status.online:
            status = "Online"
        elif user.status is discord.Status.idle:
            status = "Away"
        activity = user.activity
        if user.activity is None:
            activity = "No activity"
        else:
            if user.activity.type == ActivityType.listening:
                activity = f"Listening to {user.activity.name}"
            elif user.activity.type == ActivityType.streaming:
                activity = f"Streaming {user.activity.name}"
            elif user.activity.type == ActivityType.watching:
                activity = f"Watching {user.activity.name}"
            elif user.activity.type == ActivityType.playing:
                activity = f"Playing {user.activity.name}"
            else:
                activity = "Unknown activity"
        account_made = user.created_at.strftime("%d-%m-%Y")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="» **Information** «", value=f"**Name:** {user.name}#{user.discriminator}\n **Mention:** {user.mention}\n **ID:** {user.id}\n**Activity:** {activity}\n**Bot Account Status:** {user.bot}\n**Animated Avatar:** {user.is_avatar_animated()}\n**Account Made:** {account_made} ({(ctx.message.created_at - user.created_at).days} days ago)\n**Avatar:** [Avatar URL]({user.avatar_url})\n**Current Status:** {status}", inline=True)
        if member != None:
            account_joined = member.joined_at.strftime("%d-%m-%Y")
            role_list = [role.mention for role in reversed(member.roles) if role is not ctx.guild.default_role]
            role_list_formatted = ", ".join(role_list)
            if len(role_list) > 40:
                role_list_formatted = "Too many roles"
            elif len(role_list) == 0:
                role_list_formatted = "This user does not have any roles in this server."
            embed.add_field(name="» **Member Info** «", value=f"**Member Nickname:** {member.nick}\n**Joined At:** {account_joined} ({(ctx.message.created_at - member.joined_at).days} days ago)\n**Roles:** {role_list_formatted}", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(moderation(bot))