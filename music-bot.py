import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import asyncio
import os

BOT_PREFIX = 'cod.'
bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print("-------------------------------------------")
    print(f'{bot.user} Online!')
    print(f'{len(bot.guilds)} sunucuda toplam {str(len(set(bot.get_all_members())))} kullanıcının erişimi var.')
    for guild in bot.guilds:
        print(f'Botun aktif olduğu sunucular: {guild.name} (id:{guild.id})')
        if guild == "GUILD":
            break
    print(f'Ping: {round(bot.latency * 1000)}')
    await bot.change_presence(activity=discord.Game(name=f'COD Müzik Bot [{BOT_PREFIX}yardımmüzik] | created by zek'))
    print("-------------------------------------------")


@bot.command()
async def yardımmüzik(ctx):
    embed = discord.Embed(title=":notes: Müzik Bot Komutları",
                          colour=ctx.message.author.color, url='https://twitter.com/l3adscript')
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name=f'{BOT_PREFIX}çal [link/şarkı adı]', value="Girilen Şarkıyı Çalar", inline=False)
    embed.add_field(name=f'{BOT_PREFIX}çık', value="Bot Odadan Çıkar", inline=False)
    await ctx.send(embed=embed)


youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def çal(self, ctx, *, url):
        """Dosyayı indirmeden direk oynatır"""
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'**Müzik Çalıyor** :headphones: {player.title}')

    @commands.command()
    async def çık(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send("**Odadan Kovdular** :sob:")
        else:
            await ctx.send("**Beni aranıza zaten almadınız ki** :sob:")

    @çal.error
    async def çal_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f':sound: **{BOT_PREFIX}çal [link veya şarkı adı]** şeklinde kullanın.')

    @çal.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(":mag_right: **Herhangi bi Ses Kanalında Değilsin!**")
                raise commands.CommandError("Herhangi bi Ses Kanalında Değilsin!")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot.add_cog(Music(bot))
bot.run(os.environ.get('musictoken'))
