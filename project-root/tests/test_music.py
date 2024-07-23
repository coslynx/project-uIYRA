import pytest
import discord
from discord.ext import commands
from unittest.mock import patch, MagicMock
from bot.cogs.music import MusicCog
from utils.music_utils import get_song_info, get_audio_stream, play_audio, stop_audio

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
    bot.add_cog(MusicCog(bot))
    return bot

@pytest.fixture
def ctx():
    ctx = MagicMock(spec=commands.Context)
    ctx.author = MagicMock(voice=MagicMock(channel=MagicMock()))
    ctx.guild = MagicMock(id=1234567890)
    return ctx

@patch('utils.music_utils.get_song_info')
def test_play(mock_get_song_info, bot, ctx):
    mock_get_song_info.return_value = {'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
    bot.get_cog('MusicCog').play(ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_get_song_info.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert ctx.send.call_args[0][0] == 'Added Song Title to the queue.'

@patch('utils.music_utils.get_song_info')
@patch('bot.cogs.music.MusicCog.join')
def test_play_with_no_voice_client(mock_join, mock_get_song_info, bot, ctx):
    mock_get_song_info.return_value = {'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
    bot.get_cog('MusicCog').voice_client = None
    bot.get_cog('MusicCog').play(ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_join.assert_called_once_with(ctx)
    mock_get_song_info.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert ctx.send.call_args_list[1][0][0] == 'Added Song Title to the queue.'

@patch('utils.music_utils.get_song_info')
@patch('bot.cogs.music.MusicCog.play_next')
def test_play_with_empty_queue(mock_play_next, mock_get_song_info, bot, ctx):
    mock_get_song_info.return_value = {'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
    bot.get_cog('MusicCog').queue = []
    bot.get_cog('MusicCog').play(ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_get_song_info.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_play_next.assert_called_once_with(ctx)
    assert ctx.send.call_args_list[1][0][0] == 'Added Song Title to the queue.'

@patch('utils.music_utils.get_audio_stream')
@patch('bot.cogs.music.MusicCog.play_next')
def test_play_next(mock_play_next, mock_get_audio_stream, bot, ctx):
    bot.get_cog('MusicCog').queue = [{'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}]
    bot.get_cog('MusicCog').voice_client = MagicMock()
    bot.get_cog('MusicCog').play_next(ctx)
    mock_get_audio_stream.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_play_next.assert_not_called()
    bot.get_cog('MusicCog').voice_client.play.assert_called_once()
    assert ctx.send.call_args[0][0] == 'Now playing: Song Title by Artist Name'

@patch('utils.music_utils.get_audio_stream')
@patch('bot.cogs.music.MusicCog.play_next')
def test_play_next_with_download_error(mock_play_next, mock_get_audio_stream, bot, ctx):
    mock_get_audio_stream.side_effect = youtube_dl.utils.DownloadError('Download Error')
    bot.get_cog('MusicCog').queue = [{'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}]
    bot.get_cog('MusicCog').voice_client = MagicMock()
    bot.get_cog('MusicCog').play_next(ctx)
    mock_get_audio_stream.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_play_next.assert_called_once_with(ctx)
    assert ctx.send.call_args[0][0] == 'Error: Could not download Song Title. Skipping.'

@patch('utils.music_utils.get_audio_stream')
@patch('bot.cogs.music.MusicCog.play_next')
def test_play_next_with_song_loop(mock_play_next, mock_get_audio_stream, bot, ctx):
    mock_get_audio_stream.return_value = MagicMock()
    bot.get_cog('MusicCog').queue = [{'title': 'Song Title', 'artist': 'Artist Name', 'thumbnail': 'https://i.imgur.com/gWv3uX0.png', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}]
    bot.get_cog('MusicCog').voice_client = MagicMock()
    bot.get_cog('MusicCog').song_loop = True
    bot.get_cog('MusicCog').play_next(ctx)
    mock_get_audio_stream.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    mock_play_next.assert_called_once_with(ctx)
    bot.get_cog('MusicCog').voice_client.play.assert_called_once()
    assert ctx.send.call_args_list[1][0][0] == 'Now playing: Song Title by Artist Name'

def test_pause(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_playing=MagicMock(return_value=True))
    bot.get_cog('MusicCog').pause(ctx)
    bot.get_cog('MusicCog').voice_client.pause.assert_called_once()
    assert ctx.send.call_args[0][0] == 'Paused.'

def test_pause_with_no_song_playing(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_playing=MagicMock(return_value=False))
    bot.get_cog('MusicCog').pause(ctx)
    bot.get_cog('MusicCog').voice_client.pause.assert_not_called()
    assert ctx.send.call_args[0][0] == 'No song is playing.'

def test_resume(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_paused=MagicMock(return_value=True))
    bot.get_cog('MusicCog').resume(ctx)
    bot.get_cog('MusicCog').voice_client.resume.assert_called_once()
    assert ctx.send.call_args[0][0] == 'Resumed.'

def test_resume_with_no_song_paused(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_paused=MagicMock(return_value=False))
    bot.get_cog('MusicCog').resume(ctx)
    bot.get_cog('MusicCog').voice_client.resume.assert_not_called()
    assert ctx.send.call_args[0][0] == 'No song is paused.'

def test_stop(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock()
    bot.get_cog('MusicCog').stop(ctx)
    bot.get_cog('MusicCog').voice_client.stop.assert_called_once()
    assert ctx.send.call_args[0][0] == 'Stopped.'

def test_stop_with_no_voice_client(bot, ctx):
    bot.get_cog('MusicCog').voice_client = None
    bot.get_cog('MusicCog').stop(ctx)
    assert ctx.send.call_args[0][0] == 'I am not in a voice channel.'

def test_skip(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_playing=MagicMock(return_value=True))
    bot.get_cog('MusicCog').skip(ctx)
    bot.get_cog('MusicCog').voice_client.stop.assert_called_once()
    assert ctx.send.call_args[0][0] == 'Skipped.'

def test_skip_with_no_song_playing(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(is_playing=MagicMock(return_value=False))
    bot.get_cog('MusicCog').skip(ctx)
    bot.get_cog('MusicCog').voice_client.stop.assert_not_called()
    assert ctx.send.call_args[0][0] == 'No song is playing.'

def test_queue(bot, ctx):
    bot.get_cog('MusicCog').queue = [{'title': 'Song 1'}, {'title': 'Song 2'}]
    bot.get_cog('MusicCog').queue(ctx)
    assert ctx.send.call_args[0][0] == '```\n1. Song 1\n2. Song 2\n```'

def test_queue_with_empty_queue(bot, ctx):
    bot.get_cog('MusicCog').queue = []
    bot.get_cog('MusicCog').queue(ctx)
    assert ctx.send.call_args[0][0] == 'The queue is empty.'

def test_clear(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock()
    bot.get_cog('MusicCog').queue = [{'title': 'Song 1'}, {'title': 'Song 2'}]
    bot.get_cog('MusicCog').clear(ctx)
    assert bot.get_cog('MusicCog').queue == []
    assert ctx.send.call_args[0][0] == 'Cleared the queue.'

def test_clear_with_no_voice_client(bot, ctx):
    bot.get_cog('MusicCog').voice_client = None
    bot.get_cog('MusicCog').queue = [{'title': 'Song 1'}, {'title': 'Song 2'}]
    bot.get_cog('MusicCog').clear(ctx)
    assert ctx.send.call_args[0][0] == 'I am not in a voice channel.'

def test_volume(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(source=MagicMock())
    bot.get_cog('MusicCog').volume(ctx, 50)
    assert bot.get_cog('MusicCog').voice_client.source.volume == 0.5
    assert ctx.send.call_args[0][0] == 'Volume set to 50%.'

def test_volume_with_invalid_volume(bot, ctx):
    bot.get_cog('MusicCog').voice_client = MagicMock(source=MagicMock())
    bot.get_cog('MusicCog').volume(ctx, 150)
    assert ctx.send.call_args[0][0] == 'Volume must be between 0 and 100.'

def test_loop_on(bot, ctx):
    bot.get_cog('MusicCog').loop(ctx, 'on')
    assert bot.get_cog('MusicCog').song_loop is True
    assert ctx.send.call_args[0][0] == 'Song loop enabled.'

def test_loop_off(bot, ctx):
    bot.get_cog('MusicCog').song_loop = True
    bot.get_cog('MusicCog').loop(ctx, 'off')
    assert bot.get_cog('MusicCog').song_loop is False
    assert ctx.send.call_args[0][0] == 'Song loop disabled.'

def test_loop_invalid_mode(bot, ctx):
    bot.get_cog('MusicCog').loop(ctx, 'invalid')
    assert ctx.send.call_args[0][0] == "Invalid loop mode. Use 'on' or 'off'."

def test_cog_command_error(bot, ctx):
    error = Exception('Test Error')
    bot.get_cog('MusicCog').cog_command_error(ctx, error)
    assert ctx.send.call_args[0][0] == f'An error occurred: {error}'