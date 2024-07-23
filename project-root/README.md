# Discord Music Bot

This project is a Discord bot designed to provide music playback functionalities for users on Discord servers. It allows users to listen to music from various sources like YouTube, Spotify, and SoundCloud, manage playlists, and control playback with a simple command-based interface.

## Features

- **Music Playback:** Play, pause, stop, skip, and adjust the volume of music from multiple sources.
- **Playlist Management:** Create, manage, and share playlists with friends.
- **Voice Channel Integration:** Seamlessly integrate with Discord's voice channels.
- **User-Friendly Commands:** Intuitive command system for easy interaction.
- **Server Management:**  Admins can control bot settings, permissions, and music sources.
- **Database Integration:** Persistent data storage for server settings, playlists, and user preferences.
- **Error Handling:** Robust error handling mechanisms for a stable and reliable bot.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/discord-music-bot.git
   ```

2. **Install dependencies:**
   ```bash
   cd discord-music-bot
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:**
   Create a file named `.env` in the project root directory and add the following environment variables:

   ```
   DISCORD_TOKEN=your_discord_bot_token
   DATABASE_URL=postgresql://your_username:your_password@your_host:your_port/your_database_name
   REDIS_URL=redis://your_redis_host:your_redis_port
   YOUTUBE_API_KEY=your_youtube_data_api_key (optional)
   SPOTIFY_CLIENT_ID=your_spotify_client_id (optional)
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret (optional)
   SOUNDCLOUD_CLIENT_ID=your_soundcloud_client_id (optional)
   SOUNDCLOUD_CLIENT_SECRET=your_soundcloud_client_secret (optional)
   ```

4. **Set up the database:**
   - Create a PostgreSQL database.
   - Create a database user with appropriate permissions.
   - Set the `DATABASE_URL` environment variable in your `.env` file.
   - Run the SQL schema in `database/schema.sql` to create the necessary tables.

5. **Run the bot:**
   ```bash
   python bot/main.py
   ```

## Hosting

You can host the bot on various cloud platforms like Heroku, AWS, or Google Cloud. Here's a general guide for hosting on Heroku:

1. **Create a new Heroku app:**
   - Log in to your Heroku account and create a new app.

2. **Connect your repository:**
   - Link your GitHub repository to the Heroku app.

3. **Set environment variables:**
   - Go to the "Settings" tab of your Heroku app and add the environment variables from your `.env` file.

4. **Configure the `Procfile`:**
   Create a `Procfile` in the project root directory with the following content:
   ```
   web: python bot/main.py
   ```

5. **Deploy the bot:**
   - Click the "Deploy" tab on your Heroku app and choose "GitHub" as the deployment method.
   - Deploy the bot by clicking the "Deploy Branch" button.

6. **Enable automatic deployments:**
   - Go to the "Deploy" tab and enable automatic deployments for your repository's main branch.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.