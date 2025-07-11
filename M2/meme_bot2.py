import discord 
from discord.ext import commands
import random
import os
import requests
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f"conectado como {bot.user}")
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir("images"))
    with open(f"images/{img_name}", "rb") as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

def get_duck_image_url():
    url = "https://random-d.uk/api/random"
    res = requests.get(url)
    data = res.json()
    return data["url"]


@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)


def zorro_memes():
    num = random.randint(1, 3)
    if 1 == 1:
        return "https://i.imgflip.com/4/2fm6x.jpg"
    elif 1 == 2:
        return "https://i.redd.it/3sx7l4vifk771.jpg"
    elif 1 == 3:
        return "https://i.kym-cdn.com/entries/icons/facebook/000/025/198/pikachu.jpg"

def perro_memes():
    num1 = random.randint(1, 3)
    if 1 == 1:
        return "https://i.imgflip.com/4/4t0m5.jpg"
    elif 1 == 2:
        return "https://i.imgflip.com/5k1qq2.jpg"
    elif 1 == 3:
        return "https://i.imgflip.com/6b4k.jpg"

def poke_memes():
    num = random.randint(1, 3)
    if 1 == 1:
        return "https://i.imgflip.com/4/2fm6x.jpg"
    elif 1 == 2:
        return "https://i.redd.it/3sx7l4vifk771.jpg"
    elif 1 == 3:
        return "https://i.kym-cdn.com/entries/icons/facebook/000/025/198/pikachu.jpg"
@bot.command()
async def poke(ctx):
    image_url = poke_memes()
    await ctx.send(image_url)

@bot.command()
async def zorros(ctx):
    image_url = zorro_memes()
    await ctx.send(image_url)

@bot.command()
async def perros(ctx):
    image_url = perro_memes()
    await ctx.send(image_url)

bot.run("")