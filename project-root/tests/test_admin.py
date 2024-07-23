import pytest
import discord
from discord.ext import commands
from unittest.mock import patch, MagicMock
from bot.cogs.admin import AdminCog
from utils.config_utils import load_config
from utils.database_utils import get_server_settings, update_server_settings

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
    bot.add_cog(AdminCog(bot))
    return bot

@pytest.fixture
def ctx():
    ctx = MagicMock(spec=commands.Context)
    ctx.guild = MagicMock(id=1234567890)
    ctx.author = MagicMock(permissions=discord.Permissions.all())
    return ctx

@patch('utils.database_utils.get_server_settings')
@patch('utils.database_utils.update_server_settings')
def test_set_prefix(mock_update_server_settings, mock_get_server_settings, bot, ctx):
    mock_get_server_settings.return_value = {'DEFAULT_PREFIX': '!'}
    bot.get_cog('AdminCog').set_prefix(ctx, '>')
    mock_get_server_settings.assert_called_once_with(ctx.guild.id)
    mock_update_server_settings.assert_called_once_with(ctx.guild.id, {'DEFAULT_PREFIX': '>'})
    assert ctx.send.call_args[0][0] == "Command prefix set to `>`."

@patch('utils.database_utils.get_server_settings')
@patch('utils.database_utils.update_server_settings')
def test_set_default_source(mock_update_server_settings, mock_get_server_settings, bot, ctx):
    mock_get_server_settings.return_value = {'DEFAULT_SOURCE': 'youtube'}
    bot.get_cog('AdminCog').set_default_source(ctx, 'spotify')
    mock_get_server_settings.assert_called_once_with(ctx.guild.id)
    mock_update_server_settings.assert_called_once_with(ctx.guild.id, {'DEFAULT_SOURCE': 'spotify'})
    assert ctx.send.call_args[0][0] == "Default music source set to `spotify`."

@patch('utils.database_utils.get_server_settings')
@patch('utils.database_utils.update_server_settings')
def test_add_source(mock_update_server_settings, mock_get_server_settings, bot, ctx):
    mock_get_server_settings.return_value = {'ALLOWED_SOURCES': ['youtube', 'spotify']}
    bot.get_cog('AdminCog').add_source(ctx, 'soundcloud')
    mock_get_server_settings.assert_called_once_with(ctx.guild.id)
    mock_update_server_settings.assert_called_once_with(ctx.guild.id, {'ALLOWED_SOURCES': ['youtube', 'spotify', 'soundcloud']})
    assert ctx.send.call_args[0][0] == "Music source `soundcloud` added."

@patch('utils.database_utils.get_server_settings')
@patch('utils.database_utils.update_server_settings')
def test_remove_source(mock_update_server_settings, mock_get_server_settings, bot, ctx):
    mock_get_server_settings.return_value = {'ALLOWED_SOURCES': ['youtube', 'spotify', 'soundcloud']}
    bot.get_cog('AdminCog').remove_source(ctx, 'spotify')
    mock_get_server_settings.assert_called_once_with(ctx.guild.id)
    mock_update_server_settings.assert_called_once_with(ctx.guild.id, {'ALLOWED_SOURCES': ['youtube', 'soundcloud']})
    assert ctx.send.call_args[0][0] == "Music source `spotify` removed."

@patch('utils.database_utils.get_playlists')
def test_view_playlists(mock_get_playlists, bot, ctx):
    mock_get_playlists.return_value = [{'name': 'playlist1'}, {'name': 'playlist2'}]
    bot.get_cog('AdminCog').view_playlists(ctx)
    mock_get_playlists.assert_called_once_with(ctx.guild.id)
    assert ctx.send.call_args[0][0] == "Available playlists: playlist1, playlist2"

@patch('utils.database_utils.create_playlist')
def test_create_playlist(mock_create_playlist, bot, ctx):
    bot.get_cog('AdminCog').create_playlist(ctx, 'new_playlist')
    mock_create_playlist.assert_called_once_with(ctx.guild.id, 'new_playlist')
    assert ctx.send.call_args[0][0] == "Playlist `new_playlist` created."

@patch('utils.database_utils.add_to_playlist')
def test_add_to_playlist(mock_add_to_playlist, bot, ctx):
    bot.get_cog('AdminCog').add_to_playlist(ctx, 'playlist_name', 'song_url')
    mock_add_to_playlist.assert_called_once_with(ctx.guild.id, 'playlist_name', 'song_url')
    assert ctx.send.call_args[0][0] == "Song added to playlist `playlist_name`."

@patch('utils.database_utils.remove_from_playlist')
def test_remove_from_playlist(mock_remove_from_playlist, bot, ctx):
    bot.get_cog('AdminCog').remove_from_playlist(ctx, 'playlist_name', 'song_url')
    mock_remove_from_playlist.assert_called_once_with(ctx.guild.id, 'playlist_name', 'song_url')
    assert ctx.send.call_args[0][0] == "Song removed from playlist `playlist_name`."

@patch('utils.database_utils.delete_playlist')
def test_delete_playlist(mock_delete_playlist, bot, ctx):
    bot.get_cog('AdminCog').delete_playlist(ctx, 'playlist_name')
    mock_delete_playlist.assert_called_once_with(ctx.guild.id, 'playlist_name')
    assert ctx.send.call_args[0][0] == "Playlist `playlist_name` deleted."