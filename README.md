# HIFI.PY
Spotify Discord Music Bot
The Spotify Discord music bot is a Python script that allows you to play music from your Spotify account directly in your Discord server. The bot comes with a range of commands to manage music playback, including play, skip, back, random, shuffle, repeat, stop, and volume.

## Features
Play music from your Spotify account directly in your Discord server
Manage music playback with a range of commands, including play, skip, back, random, shuffle, repeat, stop, and volume
Support for multiple languages, including English, French, and German
Comprehensive error handling to provide clear feedback to users
Queue management to add and remove songs for playback
Requirements
Python 3.6 or higher
Discord.py
Spotipy
Pydub
A Spotify developer account

## Installation
Clone the repository to your local machine.
Install the required libraries by running pip install -r requirements.txt in your command prompt or terminal.
Create a new Spotify developer account here.
Create a new app in the Spotify developer dashboard.
Add http://localhost:8888/callback as a Redirect URI in the app settings.
Note the Client ID and Client Secret for the app, as well as the Redirect URI.
Update the client_id, client_secret, and redirect_uri variables in the spotify_discord_bot.py file to match your app settings.
Run the script by running python spotify_discord_bot.py in your command prompt or terminal.
Usage
The bot is controlled through a range of commands that can be typed into any text channel in your Discord server. Here's an overview of each command:

### Play
!play <song> - Plays the specified song from your Spotify account.

### Skip
!skip - Skips to the next song in the queue.

### Back
!back - Goes back to the previous song in the queue.

### Random
!random - Plays a random song from your Spotify library.

### Shuffle
!shuffle - Shuffles the songs in the queue.

### Repeat
!repeat - Repeats the current song.

### Stop
!stop - Stops playback.

### Volume
!volume <level> - Sets the volume level. level should be a value between 0 and 100.

## Localization
The bot supports multiple languages, including English, French, and German. To change the language, simply update the language_code variable in the spotify_discord_bot.py file to the desired language code (e.g., "en" for English, "fr" for French, "de" for German). The bot will automatically load the appropriate localized texts from the localized_texts.json file.

## Error Handling
The bot includes comprehensive error handling to provide clear feedback to users when something goes wrong. Here's an overview of each error message:

Invalid command. - The user typed an invalid command.
Please provide all required arguments. - The user did not provide all required arguments for a command.
An error occurred. - An unspecified error occurred.
A song is already playing. - The user tried to play a song when a song is already playing.
No song is currently playing. - The user tried to skip, back, repeat, or stop when no song is currently playing.
The queue is empty. - The user tried