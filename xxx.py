# import necessary modules
import random
import discord
import asyncio
from discord.ext import commands
import os

# creates a bot instance with "$" as the command prefix
bot = commands.Bot("/")
client = discord.Client()



# stage changes & commit
# git fetch origin master
# git push origin master


# This is how you define a discord.py event
@bot.event
async def on_ready():  # the event `on_ready` is triggered when the bot is ready to function
    print("The bot is READY!")
    print("Logged in as: {}".format(bot.user.name))
    bot.load_extension("cogs.Fun")
    


@bot.event
async def on_command_error(ctx, e):
    if isinstance(e, commands.CommandOnCooldown):
        message = await ctx.send(f'Stop spamming! Try again in {round(e.retry_after)+1} second(s).')
    elif isinstance(e, commands.CheckFailure):
        message = await ctx.send(f"Fuck off! You're not my master!")
    elif isinstance(e, commands.CommandNotFound):
        message = await ctx.send(f"Command does not exist.")
    elif isinstance(e, commands.MissingPermissions):
        message = await ctx.send(f"You are missing these ({list.missing_perms}) to run this command.")
    elif isinstance(e, commands.BotMissingPermissions):
        message = await ctx.send(f"I need these permissions ({list.missing_perms}) to run this command.")
    elif isinstance(e, commands.CommandError):
        message = await ctx.send(f"**Error:** {e}")
    elif isinstance(e, discord.HTTPException):
        message = await ctx.send(f"**Error:** {e}")
    else:
        print(e)
        return
    await asyncio.sleep(5)
    await message.delete()
    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if random.randrange(6) == 0:
        if 'uwu' in message.content:
            await message.channel.send('uwu')
        if 'OwO' in message.content:
            await message.channel.send('whats this?')
    await bot.process_commands(message)


initial_extensions = ["cogs.Utility,cogs.Fun"]
cogs_dir = "cogs"

if __name__ == '__cogs__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))



# starts the bot with the corresponding token
bot.run(os.getenv('TOKEN'))
