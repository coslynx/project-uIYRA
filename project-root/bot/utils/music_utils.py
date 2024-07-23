import youtube_dl
import asyncio
import ffmpeg

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

async def get_song_info(url):
    """Fetches song information (title, artist, album art) from a given URL.

    Args:
        url (str): The URL of the song.

    Returns:
        dict: A dictionary containing song information.
    """
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown Title'),
            'artist': info.get('artist', 'Unknown Artist'),
            'thumbnail': info.get('thumbnail', 'https://i.imgur.com/gWv3uX0.png'),
            'url': url,
        }

async def get_audio_stream(url):
    """Returns an audio stream from a given URL.

    Args:
        url (str): The URL of the song.

    Returns:
        ffmpeg.input: An ffmpeg input object representing the audio stream.
    """
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info.get('url')
        if audio_url:
            return ffmpeg.input(audio_url, **ffmpeg_options)
        else:
            return None

async def play_audio(voice_client, audio_stream):
    """Plays audio from an audio stream.

    Args:
        voice_client (discord.VoiceClient): The voice client object.
        audio_stream (ffmpeg.input): An ffmpeg input object representing the audio stream.
    """
    if audio_stream:
        voice_client.play(audio_stream, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(voice_client), voice_client.loop).result())

async def stop_audio(voice_client):
    """Stops the current audio playback.

    Args:
        voice_client (discord.VoiceClient): The voice client object.
    """
    voice_client.stop()

async def play_next(voice_client):
    """Plays the next song in the queue."""
    # Implement logic to handle the next song in the queue (not provided in the context)
    pass