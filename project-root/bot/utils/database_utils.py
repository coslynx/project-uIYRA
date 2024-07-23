import psycopg2
from utils.config_utils import get_config

config = get_config()

def connect_to_database(database_url):
    """Establishes a connection to the PostgreSQL database.

    Args:
        database_url (str): The URL of the PostgreSQL database.

    Returns:
        psycopg2.connection: A connection object to the database.
    """
    try:
        connection = psycopg2.connect(database_url)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_server_settings(server_id):
    """Retrieves server settings from the database.

    Args:
        server_id (int): The ID of the Discord server.

    Returns:
        dict: A dictionary containing the server settings.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM server_settings WHERE server_id = %s", (server_id,)
        )
        server_settings = cursor.fetchone()
        if server_settings:
            return {
                "DEFAULT_PREFIX": server_settings[1],
                "DEFAULT_SOURCE": server_settings[2],
                "ALLOWED_SOURCES": server_settings[3].split(","),
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving server settings: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def update_server_settings(server_id, server_settings):
    """Updates server settings in the database.

    Args:
        server_id (int): The ID of the Discord server.
        server_settings (dict): A dictionary containing the updated server settings.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE server_settings SET default_prefix = %s, default_source = %s, allowed_sources = %s WHERE server_id = %s",
            (
                server_settings['DEFAULT_PREFIX'],
                server_settings['DEFAULT_SOURCE'],
                ",".join(server_settings['ALLOWED_SOURCES']),
                server_id,
            ),
        )
        connection.commit()
    except Exception as e:
        print(f"Error updating server settings: {e}")
    finally:
        cursor.close()
        connection.close()

def get_playlists(server_id):
    """Retrieves playlists from the database.

    Args:
        server_id (int): The ID of the Discord server.

    Returns:
        list: A list of dictionaries, each representing a playlist.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM playlists WHERE server_id = %s", (server_id,)
        )
        playlists = cursor.fetchall()
        return [
            {"name": playlist[1], "songs": playlist[2].split(",")}
            for playlist in playlists
        ]
    except Exception as e:
        print(f"Error retrieving playlists: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_playlist(server_id, name):
    """Creates a new playlist in the database.

    Args:
        server_id (int): The ID of the Discord server.
        name (str): The name of the new playlist.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO playlists (server_id, name) VALUES (%s, %s)",
            (server_id, name),
        )
        connection.commit()
    except Exception as e:
        print(f"Error creating playlist: {e}")
    finally:
        cursor.close()
        connection.close()

def add_to_playlist(server_id, playlist_name, url):
    """Adds a song to a playlist in the database.

    Args:
        server_id (int): The ID of the Discord server.
        playlist_name (str): The name of the playlist.
        url (str): The URL of the song to add.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT songs FROM playlists WHERE server_id = %s AND name = %s",
            (server_id, playlist_name),
        )
        playlist = cursor.fetchone()
        if playlist:
            songs = playlist[0].split(",")
            songs.append(url)
            cursor.execute(
                "UPDATE playlists SET songs = %s WHERE server_id = %s AND name = %s",
                (",".join(songs), server_id, playlist_name),
            )
            connection.commit()
        else:
            print(f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        print(f"Error adding song to playlist: {e}")
    finally:
        cursor.close()
        connection.close()

def remove_from_playlist(server_id, playlist_name, url):
    """Removes a song from a playlist in the database.

    Args:
        server_id (int): The ID of the Discord server.
        playlist_name (str): The name of the playlist.
        url (str): The URL of the song to remove.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT songs FROM playlists WHERE server_id = %s AND name = %s",
            (server_id, playlist_name),
        )
        playlist = cursor.fetchone()
        if playlist:
            songs = playlist[0].split(",")
            if url in songs:
                songs.remove(url)
                cursor.execute(
                    "UPDATE playlists SET songs = %s WHERE server_id = %s AND name = %s",
                    (",".join(songs), server_id, playlist_name),
                )
                connection.commit()
            else:
                print(f"Song '{url}' not found in playlist '{playlist_name}'.")
        else:
            print(f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        print(f"Error removing song from playlist: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_playlist(server_id, name):
    """Deletes a playlist from the database.

    Args:
        server_id (int): The ID of the Discord server.
        name (str): The name of the playlist to delete.
    """
    connection = connect_to_database(config['DATABASE_URL'])
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM playlists WHERE server_id = %s AND name = %s",
            (server_id, name),
        )
        connection.commit()
    except Exception as e:
        print(f"Error deleting playlist: {e}")
    finally:
        cursor.close()
        connection.close()