import discord
from discord.ext import commands
import random
import logging
import os

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_prefix = '!'


client = discord.Client()
client = commands.Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    print("Bot Çevrimiçi")
    print(f'Bot {client.user} kullanıma hazır.')
    print(f'Bot, {len(client.guilds)} sunucuda aktif')
    print("Bot'a " + str(len(set(client.get_all_members()))) + " kullanıcının erişimi var.")
    for guild in client.guilds:
        print(f'Botun aktif olduğu sunucular: {guild.name} (id: {guild.id})')
        if guild.name == "GUILD":
            break
    await client.change_presence(activity=discord.Game(name='YOL ÇALIŞMASI DEVAM EDİYOR | created by zek'))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Aramıza hoş geldin {member.name}.'
                                   'Ben bundan sonra senin yoldaşınım. Bana sırrını söyleyebilirsin :D')

    hosgeldin_channel = client.get_channel(725630826833903641)
    await hosgeldin_channel.send(f'Sunucumuza hoş geldin {member.name}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    merhaba_cevap = ['Selam canım bugün nasılsın?',
                'Heh geldi yine ...']
    merhaba_liste = ['merhaba','selam','sa']
    for mrb in merhaba_liste:
        if mrb in message.content.lower():
            cevap = random.choice(merhaba_cevap)
            await message.channel.send(cevap)

    if 'dgko' in message.content.lower():
        await message.channel.send("Mutlu yıllar :D")




client.run(os.environ.get('token'))
