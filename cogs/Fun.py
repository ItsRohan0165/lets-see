import random
import json
import discord
import time
import pylast
import colorgram
import re
import io
import typing
import imghdr
from datetime import datetime
from PIL import Image, ImageDraw
from discord.ext import commands
from urllib.request import urlopen, Request
from aiohttp import ClientSession
import os 


# lastfm




class Fun:
    def __init__(self, bot):
        self.bot = bot

    async def prev_attachedimg(self, ctx):
        '''Return the latest attached message'''
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
        else:
            attach_msg = await ctx.history().find(lambda m: m.attachments)
            if attach_msg is None:
                raise commands.CommandError(f"Attachment not found.")
            attachment = attach_msg.attachments[0]
        return attachment

    async def google_search(self, query, image=False):
        params = {"q": query, "key": os.getenv("API"), "cx": os.getenv("CSE")}
        search_url = "https://www.googleapis.com/customsearch/v1"
        if image:
            params["searchType"] = "image"
        async with ClientSession() as session, session.get(search_url, params=params) as result:
            return (await result.json())["items"]

    @commands.command(aliases=['g', 'search'])
    async def google(self, ctx, *, query):
        search_results = await self.google_search(query)
        google_embed = discord.Embed(description="", title="Google Search Results", color=discord.Color.red())
        for i, result in enumerate(search_results[:5], 1):
            google_embed.description += f'{i}. [{result["title"]}]({result["link"]})\n'
        await ctx.send(embed=google_embed)

    @commands.command(aliases=['gimg', 'gsearch'])
    async def image(self, ctx, *, query):
        search_results = await self.google_search(query, image=True)
        google_embed = discord.Embed(description=search_results[0]["title"], title="Google Image Search Results", color=discord.Color.red())
        google_embed.set_image(url=search_results[0]["link"])
        await ctx.send(embed=google_embed)

  
    @commands.command()
    async def convert(self, ctx, temp: float):
        '''Convert Farenheit to Celsius'''
        C = round((temp-32)/1.8, 2)
        await ctx.send(f"{temp}°F is {C}°C")

    @commands.command()
    async def define(self, ctx, *, word: str):
        '''Provide definiton from Google'''
        loading_message = await ctx.send(f"{heart} Now loading... {heart}")
        word = word.replace(' ', '_')
        req = Request(url=f"https://googledictionaryapi.eu-gb.mybluemix.net/?define={word}&lang=en")
        with urlopen(req) as res:
            definition = json.loads(res.read())[0]["meaning"]
        def_embed = discord.Embed(title=word.title(), color=discord.Color.gold())
        for part, part_def in definition.items():
            def_embed.add_field(name=f"*{part}*", value=part_def[0]["definition"])
        await loading_message.edit(content="", embed=def_embed)

  


def setup(bot):
    bot.add_cog(Fun(bot))
