import discord
from discord.ext import commands
import random
intents = discord.Intents.default()
Bot = commands.Bot(command_prefix="$", intents=intents)

decomposition_times = {
    "botella de plastico": "450 años",
    "lata de aluminio": "entre 80 y 200 años",
    "trozo de papel": "de 2 a 6 semanas",
    "tela de algodón":"1 año",
    "chicle": "5 años",
    "cigarrillo": "entre 1 y 5 años",
    "pañal": "entre 200 y 500 años",
    "latas de refresco": "entre 80 y 200 años",
    "bolsas de plastico": "entre 10 y 1000 años",
    "botellas de vidrio": "1 millón de años",
    "baterias": "entre 100 y 1000 años",
    "carton": "de 2 a 6 semanas",
    "plástico": "entre 10 y 1000 años",
    "vidrio": "1 millón de años",
    "metal": "entre 80 y 200 años",
    "papel": "de 2 a 6 semanas",
}
consejos = [
    "Recicla siempre que puedas.",
    "Usa bolsas reutilizables.",
    "Reduce el uso de plásticos de un solo uso.",
    "Apaga las luces cuando no las necesites.",
    "Usa transporte público o comparte coche.",
    "Planta un árbol.",
    "Compra productos locales y de temporada.",
    "Ahorra agua al ducharte y lavar los platos.",
    "Desconecta los aparatos electrónicos que no uses.",
    "Participa en actividades de limpieza en tu comunidad.",
    "Usa productos de limpieza ecológicos.",
    "Evita el uso de productos desechables.",
    "Recoge la basura que encuentres en la calle.",
    "Usa bombillas de bajo consumo.",
    "Haz compost con tus restos de comida.",
    "Usa una botella de agua reutilizable.",
    "Evita el uso de aerosoles.",
    "Compra productos a granel para reducir el embalaje.",
    "Usa papel reciclado.",
]


@Bot.event
async def on_ready():
    print(f"Conectado como {Bot.user}")

@Bot.command()
async def donate(ctx):
    await ctx.send("¿Quieres apoyar una causa ecológica? Visita: https://www.ecoembes.com/es/")

@Bot.command() # Comando para obtener noticias
async def news(ctx):
    await ctx.send("📰 Mantente actualizado con las últimas noticias ecológicas en: ")

@Bot.command() # Comando para obtener el tiempo de descomposición
async def decompose(ctx, *, item):
    item = item.lower()
    matches = [key for key in decomposition_times.keys() if item in key]
    if len(matches)== 1:
        item = matches[0]
    if item in decomposition_times:
        await ctx.send(f"El tiempo de descomposición de un/a {item} es: {decomposition_times[key]}")
    else:
        await ctx.send("Lo siento, no tengo información sobre ese artículo.")

@Bot.command() # Comando para obtener ayuda
async def help(ctx):
    await ctx.send("Comandos disponibles:\n"
                   "$donate - Información sobre donaciones\n"
                   "$news - Noticias ecológicas\n"
                   "$decompose <artículo> - Tiempo de descomposición de un artículo\n"
                   "$help - Mostrar este mensaje de ayuda")
@Bot.command()
async def meme(ctx): # Comando para enviar un meme
    await ctx.send("¡Aquí tienes un meme divertido para alegrar tu día! 😂\n"
                   "https://i.imgflip.com/4/2fm6x.jpg")

@Bot.command() # Comando para obtener un consejo ecológico
async def consejo(ctx):
    await ctx.send(f"💡 Consejo ecológico: {random.choice(consejos)}")

Bot.run("TOKEN")
