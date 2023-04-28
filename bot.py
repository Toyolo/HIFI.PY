import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
from dotenv import load_dotenv
from localization import get_localized_text

# Load environment variables
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
bot_token = os.getenv("DISCORD_BOT_TOKEN")

# Initialize bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Authenticate user's Spotify account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='user-read-playback-state,user-modify-playback-state,playlist-modify-private,playlist-modify-public'))

# Define queue list
queue = []

# Play music from user's Spotify account
@bot.command(name='play')
async def play(ctx, *args):
    try:
        # Check if user has a Spotify account
        results = sp.current_playback()
        track_name = results['item']['name']
        track_uri = results['item']['uri']
        track_duration = results['item']['duration_ms']
    except spotipy.exceptions.SpotifyException:
        await ctx.send(get_localized_text(ctx.guild, 'connect_spotify'))
        return
    
    # Check if a song is already playing
    if results['is_playing']:
        await ctx.send(get_localized_text(ctx.guild, 'song_already_playing'))
        return
    
    # Check if a song is specified
    if not args:
        await ctx.send(get_localized_text(ctx.guild, 'specify_song'))
        return
    
    # Add specified song to queue
    queue.append(args[0])
    
    # Play specified song
    sp.start_playback(uris=[args[0]])
    await ctx.send(get_localized_text(ctx.guild, 'now_playing').format(args[0]))

# Skip to next song in queue
@bot.command(name='skip')
async def skip(ctx):
    # Check if a song is already playing
    results = sp.current_playback()
    if not results['is_playing']:
        await ctx.send(get_localized_text(ctx.guild, 'no_song_playing'))
        return
    
    # Check if there are any songs in the queue
    if not queue:
        await ctx.send(get_localized_text(ctx.guild, 'queue_empty'))
        return
    
    # Play next song in queue
    sp.start_playback(uris=[queue.pop(0)])
    await ctx.send(get_localized_text(ctx.guild, 'now_playing').format(queue[0]))

# Go back to previous song in queue
@bot.command(name='back')
async def back(ctx):
    # Check if a song is already playing
    results = sp.current_playback()
    if not results['is_playing']:
        await ctx.send(get_localized_text(ctx.guild, 'no_song_playing'))
        return
    
    # Check if there are any songs in the queue
    if not queue:
        await ctx.send(get_localized_text(ctx.guild, 'queue_empty'))
        return
    
    # Play previous song in queue
    sp.start_playback(uris=[queue.pop(-1)])
    await ctx.send(get_localized_text(ctx.guild, 'now_playing').format(queue[-1]))

# Play a random song
@bot.command(name='random')
async def random(ctx):
    try:
        # Get a random song from user's library
        results = sp.current_user_saved_tracks(limit=50)
        if len(results['items']) == 0:
            raise Exception(get_localized_text(ctx.guild.id, "no_saved_tracks"))
        track = random.choice(results['items'])
        track_uri = track['track']['uri']
    except Exception as e:
        await ctx.send(str(e))
        return
    
    # Play random song
    try:
        sp.start_playback(uris=[track_uri])
        await ctx.send(get_localized_text(ctx.guild.id, "now_playing").format(track['track']['name']))
    except Exception as e:
        await ctx.send(get_localized_text(ctx.guild.id, "error_playback").format(str(e)))

# Shuffle the queue
@bot.command(name='shuffle')
async def shuffle(ctx):
    # Check if there are any songs in the queue
    if not queue:
        await ctx.send(get_localized_text(ctx.guild.id, "queue_empty"))
        return

    # Shuffle the queue
    random.shuffle(queue)

    await ctx.send(get_localized_text(ctx.guild.id, "queue_shuffled"))

# Repeat the current song
@bot.command(name='repeat')
async def repeat(ctx):
    # Check if a song is already playing
    try:
        results = sp.current_playback()
        if not results['is_playing']:
            raise Exception(get_localized_text(ctx.guild.id, "not_playing"))
    except Exception as e:
        await ctx.send(str(e))
        return

    # Repeat current song
    try:
        sp.repeat('track', True)
        await ctx.send(get_localized_text(ctx.guild.id, "song_repeated"))
    except Exception as e:
        await ctx.send(get_localized_text(ctx.guild.id, "error_playback").format(str(e)))

# Stop the current song
@bot.command(name='stop')
async def stop(ctx):
    # Stop current song
    try:
        sp.pause_playback()
        await ctx.send(get_localized_text(ctx.guild.id, "music_stopped"))
    except Exception as e:
        await ctx.send(get_localized_text(ctx.guild.id, "error_playback").format(str(e)))

# Change the volume of the music
@bot.command(name='volume')
async def volume(ctx, *args):
    # Check if a song is already playing
    try:
        results = sp.current_playback()
        if not results['is_playing']:
            raise Exception(get_localized_text(ctx.guild.id, "not_playing"))
    except Exception as e:
        await ctx.send(str(e))
        return

    # Check if a volume level is specified
    if not args:
        await ctx.send(get_localized_text(ctx.guild.id, "no_volume"))
        return

    # Set volume level
    try:
        volume_percent = int(args[0])
        if volume_percent < 0 or volume_percent > 100:
            raise Exception(get_localized_text(ctx.guild.id, "invalid_volume"))
        sp.volume(volume_percent)
        await ctx.send(get_localized_text(ctx.guild.id, "volume_set").format(volume_percent))
    except Exception as e:
        await ctx.send(str(e))

# Handle errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(get_localized_text(ctx.guild.id, "invalid_command"))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(get_localized_text(ctx.guild.id, "missing_argument"))
    else:
        await ctx.send(get_localized_text(ctx.guild.id, "unknown_error"))
        raise error

# Run bot
bot.run("Token")
