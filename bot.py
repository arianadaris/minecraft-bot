# bot.py
import os
import asyncio
from dotenv import load_dotenv
from discord import Game, Status
from discord.ext import commands, tasks
from server import Server, World, Command


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
IP = os.getenv('SERVER_IP')
PORT = os.getenv('SERVER_PORT')
PASSWORD = os.getenv('CLIENT_PASSWORD')

server = Server(IP, PORT)
world = World()
cmd = Command(IP, PASSWORD)
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    set_status.start()


@tasks.loop(seconds=3)
async def set_status():
    await bot.change_presence(activity=Game(f'{server.get_players()} of 36 players online.'))
    await asyncio.sleep(3)


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


@bot.command(name='dc')
async def disconnect(ctx):
    set_status.stop()
    await bot.change_presence(status=Status.offline)
    try:
        await bot.close()
        print('Minecraft Bot has disconnected from Discord.')
    except RuntimeError:
        pass


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


@bot.command()
async def convert(ctx, *args):
    await ctx.message.channel.send(f'Nether Coordinates: ```{world.convert_coords(list(args))}```')


bot.run(TOKEN)