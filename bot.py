# bot.py
import os
import asyncio
from dotenv import load_dotenv
from discord import Game
from discord.ext import commands
from server import Server


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
IP = os.getenv('SERVER_IP')
server = Server(IP)
bot = commands.Bot(command_prefix='!')


async def status_task():
    while True:
        await bot.change_presence(activity=Game(f'{server.get_players()} of 36 players online.'))
        await asyncio.sleep(3)
        await bot.change_presence(activity=Game(f'{server.get_players()} of 36 players online.'))
        await asyncio.sleep(3)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(status_task())


@bot.command(name='status')
async def check_status(ctx):
    if server.check_status():
        await ctx.message.channel.send('The server is online.')
    else: 
        await ctx.message.channel.send('The server is offline.')


@bot.command(name='who')
async def get_online_players(ctx):
    if server.get_players() == 0:
        await ctx.message.channel.send('There are no players on the server.')
    else:
        if server.get_players() == 1:
            await ctx.message.channel.send(f'There is 1 player on the server: {server.get_player_names()}')
        else:
            await ctx.message.channel.send(f'There are {server.get_players()} players on the server: {", ".join(server.get_player_names())}')


bot.run(TOKEN)