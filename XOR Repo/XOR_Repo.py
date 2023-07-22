import discord
from discord.ext import commands 
import asyncio
import nest_asyncio 
nest_asyncio.apply()
import time
from datetime import datetime, timedelta

# BEGIN
bot = commands.Bot(command_prefix = '?', intents=discord.Intents.all(), help_command = None)
TOKEN = 'MTEyODIyMjUwMTUwNDI4Njc2Mw.G0YQzj.aG80eFJwrMDcwUMIjdJ9giJ8W737hRmxXJf9Ug'

@bot.event
async def on_ready(): 
    print("Logged in as {0.user}".format(bot))
    print("----------------------------------------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='?help'))
    print("Type ?help to see a list of commands.")

class CustomMessage:
    def __init__(self, message: discord.Message, deleted_at: datetime):
        self.guild: discord.Guild = message.guild
        self.channel: discord.TextChannel = message.channel
        self.author: discord.Member = message.author
        self.created_at: datetime = message.created_at
        self.attachments: list[discord.Attachment] = message.attachments
        self.attachment: list[discord.Attachment] = message.attachments
        self.content: str = message.content
        self.deleted_at: datetime = deleted_at
        bot.sniped_messages: dict[int, CustomMessage] = {}
            
@bot.command()
async def help(ctx):
    # defining embed
    embed = discord.Embed(color=discord.Color.green())
    embed.title = 'Commands List'
    embed.add_field(name='dm', value=f'Sends a message to a particular user\nUsage : ``?dm @user <message>``', inline=False)
    embed.add_field(name='dmall', value=f'Sends a message to everyone in the server\nUsage : ``?dmall <message>``', inline=False)
    embed.add_field(name='snipe', value=f'Reveals any message deleted within the last 5 minutes\nUsage : ``?snipe``', inline=False)
    embed.add_field(name='send', value=f'Sends a message in a given channel\nUsage : ``?send <message>``', inline=False)
    embed.add_field(name='clear', value=f'Deletes a specified number of messages\nUsage : ``?clear <number>``', inline=False)
    embed.add_field(name='ping', value=f'Shows the latency of the bot\nUsage : ``?ping``', inline=False)
    embed.add_field(name='help', value=f'Shows this message\nUsage : ``?help``', inline=False)
    embed.add_field(name='official server', value='click [here](https://discord.gg/9T4tq5WGSJ)')
    
    # Generate footer
    embed.set_footer(text=f'Made with Python 3.9')
    
    # Send embedded message
    await ctx.author.send(embed=embed)
    
    # Delete original message
    await ctx.message.delete()
    
@bot.command()
async def unlock(ctx):
    embed = discord.Embed(color=discord.Color.red())
    embed.title = '🔓 You have unlocked a secret command! 🔓'
    embed.add_field(name='dmuke', value=f'Infinitely spams a specific message to a user\'s dms\nUsage : ``?dmuke @user <message>``', inline=False)
    embed.set_footer(text=f'Use with caution! 😈')
    
    await ctx.author.send(embed=embed)
    
    await ctx.message.delete()
    
@bot.listen()
async def on_message_delete(message):
    # Cache the deleted message to be "sniped" later

    bot.sniped_messages[message.guild.id] = CustomMessage(
        message, deleted_at=discord.utils.utcnow())
    
@bot.command()
async def snipe(ctx: commands.Context):

    # fetch the last sniped messaged and check if it's older than 5 minutes
    before_timestamp = discord.utils.utcnow() - timedelta(minutes=5)
    message: CustomMessage = bot.sniped_messages.get(ctx.guild.id)
    if not message or message.deleted_at < before_timestamp:
        return await ctx.send("Nothing to snipe.")

    embed = discord.Embed(
        description=message.content, color=discord.Color.teal(), timestamp=message.created_at
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.set_footer(text=message.channel.name)

    if message.attachments and message.attachment[0].content_type in (
        "image/avif",
        "image/jpeg",
        "image/png",
    ):
        embed.set_image(url=message.attachments[0].proxy_url)
    
    await ctx.send(embed=embed)
    

@bot.command()
async def dmall(ctx, *, message:str=None):
    delay = 1
    server = ctx.guild
    member_count = len(server.members)
    if member_count < 10:
        delay = 1
    else:
        delay = 5
    if message is None:
        await ctx.send(f'{ctx.author.mention}, please enter a message to send to everybody.', delete_after=2.5)
        await ctx.message.delete()
        return
    
    for member in server.members:
        if member.bot and member != bot.user:
            await ctx.author.send(f'⚠️ Didnt message {member.name} because its a bot.')
        elif member == bot.user:
            await ctx.author.send('⚠️ Couldnt message the bot itself')
        else:
            try:
                await member.send(message)
                await ctx.author.send(f'✅ Messaged {member.name}')
            except:
                await ctx.author.send(f'⚠️ Could not message {member.name}')
            await asyncio.sleep(delay)
            
@bot.command()
async def dm(ctx, member:discord.Member=None, *, message:str=None):
    if message is None:
        await ctx.send(f'{ctx.author.mention}, please enter a message to send.', delete_after = 2.5)
        await ctx.message.delete()
        return
    if member.bot or member == bot.user:
        await ctx.message.delete()
        await ctx.author.send('⚠️ Cannot dm that user.')
        return
    else:
        try:
            await member.send(message)
            await ctx.author.send(f'✅ Messaged {member.name}')
        except:
            await ctx.author.send('⚠️ Couldnt message that user.')
            
@bot.command()
async def dmuke(ctx, member:discord.Member=None, *, message:str=None):
    if message is None:
        await ctx.send(f'{ctx.author.mention}, please enter a message to spam.', delete_after = 2.5)
        await ctx.message.delete()
        return
    if member.bot or member == bot.user:
        await ctx.message.delete()
        await ctx.author.send('⚠️ Cannot dm that user.')
        return
    else:
        await ctx.message.delete()
        try:
            await ctx.author.send(f'✅ Messaged {member.name}')
            while True:
                await member.send(message)
        except:
            await ctx.author.send('⚠️ Couldnt message that user.')
            
@bot.command()
async def send(ctx, *, message:str=None):
    if message is None:
        await ctx.send(f'{ctx.author.mention}, please enter a message to send.', delete_after = 2.5)
        await ctx.message.delete()
        return
    else:
        await ctx.message.delete()
        await ctx.send(message)
        
@bot.command()
async def clear(ctx, amount):
    try:    
        amount = int(amount)
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send('Messages successfully cleared.', delete_after = 2.5)
        await ctx.message.delete()
    except ValueError:
        await ctx.send(f'{ctx.author.mention}, please enter a number of messages to clear.', delete_after = 2.5)
        await ctx.message.delete()
        return

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, please enter a number of messages to clear.', delete_after = 2.5)
        await ctx.message.delete()
        return

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000, 2)}')
      
bot.run(TOKEN)
