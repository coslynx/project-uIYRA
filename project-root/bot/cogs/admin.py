import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from utils.config_utils import load_config
from utils.database_utils import get_server_settings, update_server_settings


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.config = load_config()

    @commands.command(name="setprefix", help="Sets the command prefix for the server.")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        server_settings = get_server_settings(ctx.guild.id)
        server_settings['DEFAULT_PREFIX'] = prefix
        update_server_settings(ctx.guild.id, server_settings)
        await ctx.send(f"Command prefix set to `{prefix}`.")

    @commands.command(name="setdefaultsource", help="Sets the default music source for the server.")
    @commands.has_permissions(administrator=True)
    async def set_default_source(self, ctx, source):
        valid_sources = ["youtube", "spotify", "soundcloud"]
        if source.lower() not in valid_sources:
            await ctx.send(f"Invalid music source. Valid sources are: {', '.join(valid_sources)}")
            return

        server_settings = get_server_settings(ctx.guild.id)
        server_settings['DEFAULT_SOURCE'] = source.lower()
        update_server_settings(ctx.guild.id, server_settings)
        await ctx.send(f"Default music source set to `{source}`.")

    @commands.command(name="addsource", help="Adds a new music source to the server.")
    @commands.has_permissions(administrator=True)
    async def add_source(self, ctx, source):
        valid_sources = ["youtube", "spotify", "soundcloud"]
        if source.lower() not in valid_sources:
            await ctx.send(f"Invalid music source. Valid sources are: {', '.join(valid_sources)}")
            return

        server_settings = get_server_settings(ctx.guild.id)
        if source.lower() in server_settings['ALLOWED_SOURCES']:
            await ctx.send(f"Music source `{source}` is already allowed.")
            return

        server_settings['ALLOWED_SOURCES'].append(source.lower())
        update_server_settings(ctx.guild.id, server_settings)
        await ctx.send(f"Music source `{source}` added.")

    @commands.command(name="removesource", help="Removes a music source from the server.")
    @commands.has_permissions(administrator=True)
    async def remove_source(self, ctx, source):
        valid_sources = ["youtube", "spotify", "soundcloud"]
        if source.lower() not in valid_sources:
            await ctx.send(f"Invalid music source. Valid sources are: {', '.join(valid_sources)}")
            return

        server_settings = get_server_settings(ctx.guild.id)
        if source.lower() not in server_settings['ALLOWED_SOURCES']:
            await ctx.send(f"Music source `{source}` is not allowed.")
            return

        server_settings['ALLOWED_SOURCES'].remove(source.lower())
        update_server_settings(ctx.guild.id, server_settings)
        await ctx.send(f"Music source `{source}` removed.")

    @commands.command(name="viewplaylists", help="Displays all available playlists.")
    @commands.has_permissions(administrator=True)
    async def view_playlists(self, ctx):
        playlists = get_playlists(ctx.guild.id)
        if not playlists:
            await ctx.send("No playlists found.")
            return

        playlist_names = [playlist['name'] for playlist in playlists]
        await ctx.send(f"Available playlists: {', '.join(playlist_names)}")

    @commands.command(name="createplaylist", help="Creates a new playlist.")
    @commands.has_permissions(administrator=True)
    async def create_playlist(self, ctx, name):
        create_playlist(ctx.guild.id, name)
        await ctx.send(f"Playlist `{name}` created.")

    @commands.command(name="addtoplaylist", help="Adds a song to a playlist.")
    @commands.has_permissions(administrator=True)
    async def add_to_playlist(self, ctx, playlist_name, url):
        add_to_playlist(ctx.guild.id, playlist_name, url)
        await ctx.send(f"Song added to playlist `{playlist_name}`.")

    @commands.command(name="removefromplaylist", help="Removes a song from a playlist.")
    @commands.has_permissions(administrator=True)
    async def remove_from_playlist(self, ctx, playlist_name, url):
        remove_from_playlist(ctx.guild.id, playlist_name, url)
        await ctx.send(f"Song removed from playlist `{playlist_name}`.")

    @commands.command(name="deleteplaylist", help="Deletes a playlist.")
    @commands.has_permissions(administrator=True)
    async def delete_playlist(self, ctx, name):
        delete_playlist(ctx.guild.id, name)
        await ctx.send(f"Playlist `{name}` deleted.")


def setup(bot):
    bot.add_cog(AdminCog(bot))