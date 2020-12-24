# bot.py
import os
import asyncio
from dotenv import load_dotenv
from discord import Game
from discord.ext import commands
from server import Server, World


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
IP = os.getenv('SERVER_IP')
server = Server(IP)
world = World()
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
    player_count = server.get_players()
    if player_count == 0:
        await ctx.message.channel.send('There are no players on the server.')
    else:
        players = "".join(server.get_player_names())
        if server.get_players() == 1:
            await ctx.message.channel.send(f'There is 1 player on the server: ```{players}```')
        else:
            await ctx.message.channel.send(f'There are {player_count} players on the server: ```{players}```')


@bot.command()
async def save(ctx, *args):
    if world.save_coords(list(args)):
        await ctx.message.channel.send('I have saved the coordinates.')
    else:
        await ctx.message.channel.send('Coordinates could not be saved.')


@bot.command()
async def coords(ctx, *args):
    if not world.check_coords_file():
        await ctx.message.channel.send('No saved coordinates to load.')
    else:
        coords = "".join(world.load_coords())
        await ctx.message.channel.send(f'Coordinates:```{coords}```')


bot.run(TOKEN)