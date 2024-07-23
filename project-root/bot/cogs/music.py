import discord
from discord.ext import commands
import youtube_dl
import asyncio
from utils.music_utils import get_song_info, get_audio_stream, play_audio, stop_audio
import os

ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn -af "volume=1" -loglevel quiet',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current_song = None
        self.voice_client = None
        self.song_loop = False

    @commands.command(name='join', help='Joins the voice channel you are in.')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.author.voice.channel
        if self.voice_client:
            await self.voice_client.disconnect()

        self.voice_client = await channel.connect()

        await ctx.send(f'Joined {channel.name}')

    @commands.command(name='leave', help='Leaves the voice channel.')
    async def leave(self, ctx):
        if self.voice_client:
            await self.voice_client.disconnect()
            self.queue = []
            self.current_song = None
            await ctx.send("Disconnected from voice channel.")
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command(name='play', help='Plays music from a given URL or file path.')
    async def play(self, ctx, url):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        if self.voice_client is None:
            await self.join(ctx)

        if url is None:
            await ctx.send("Please provide a valid URL or file path.")
            return

        try:
            song_info = await get_song_info(url)
        except youtube_dl.utils.DownloadError:
            await ctx.send(f"Error: Invalid URL or file path. Please try again.")
            return

        self.queue.append(song_info)

        if self.current_song is None:
            await self.play_next(ctx)

        await ctx.send(f"Added {song_info['title']} to the queue.")

    @commands.command(name='pause', help='Pauses the current song.')
    async def pause(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send("Paused.")
        else:
            await ctx.send("No song is playing.")

    @commands.command(name='resume', help='Resumes the current song.')
    async def resume(self, ctx):
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("No song is paused.")

    @commands.command(name='stop', help='Stops the current song and clears the queue.')
    async def stop(self, ctx):
        if self.voice_client:
            self.voice_client.stop()
            self.queue = []
            self.current_song = None
            await ctx.send("Stopped.")
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command(name='skip', help='Skips the current song.')
    async def skip(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            await self.play_next(ctx)
            await ctx.send("Skipped.")
        else:
            await ctx.send("No song is playing.")

    @commands.command(name='queue', help='Shows the current music queue.')
    async def queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("The queue is empty.")
            return

        queue_str = "```\n"
        for i, song in enumerate(self.queue):
            queue_str += f"{i+1}. {song['title']}\n"
        queue_str += "```"
        await ctx.send(queue_str)

    @commands.command(name='clear', help='Clears the current music queue.')
    async def clear(self, ctx):
        if self.voice_client:
            self.voice_client.stop()
            self.queue = []
            self.current_song = None
            await ctx.send("Cleared the queue.")
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command(name='volume', help='Sets the playback volume. (0-100)')
    async def volume(self, ctx, volume: int):
        if not self.voice_client:
            await ctx.send("I am not in a voice channel.")
            return

        if 0 <= volume <= 100:
            self.voice_client.source.volume = volume / 100
            await ctx.send(f"Volume set to {volume}%")
        else:
            await ctx.send("Volume must be between 0 and 100.")

    @commands.command(name='loop', help='Loops the current song. (on/off)')
    async def loop(self, ctx, loop_mode):
        if loop_mode.lower() == 'on':
            self.song_loop = True
            await ctx.send("Song loop enabled.")
        elif loop_mode.lower() == 'off':
            self.song_loop = False
            await ctx.send("Song loop disabled.")
        else:
            await ctx.send("Invalid loop mode. Use 'on' or 'off'.")

    async def play_next(self, ctx):
        if len(self.queue) > 0:
            self.current_song = self.queue.pop(0)
            try:
                audio_stream = await get_audio_stream(self.current_song['url'])
            except youtube_dl.utils.DownloadError:
                await ctx.send(f"Error: Could not download {self.current_song['title']}. Skipping.")
                return await self.play_next(ctx)

            self.voice_client.play(audio_stream, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result())
            await ctx.send(f"Now playing: {self.current_song['title']} by {self.current_song['artist']}")

            while self.song_loop:
                if not self.voice_client.is_playing():
                    await self.play_next(ctx)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f'An error occurred: {error}')

def setup(bot):
    bot.add_cog(MusicCog(bot))