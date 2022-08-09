import discord
from replit import db
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import weather_func as wf
import pyjokes
import caesarCy_art
from cy_func import coder

load_dotenv()
TOKEN = os.getenv('TOKEN')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')


# Initialising DB, by default, units are celsius and atm, city is Bangalore.


if "units" not in db.keys():
    db["units"] = "CA"

# for favorites.

if "fav" not in db.keys():
    db["fav"] = []

# for default city.

if "defCity" not in db.keys():
    db["defCity"] = "Bangalore"

mode = "howto"
dash = "-"
usage = "How to use"


howto = f'''--> We are currently in a default state,\nYou can select a mode by typing in ==> MODE weather, MODE suggest, MODE cypher [case-sensitive].\n{dash:-^50}\nOnce you are in weather mode, type in $capabilities.\n{dash:-^50}\nOnce you are in suggest mode, type in $use\n{dash:-^50}\nOnce you are in cypher mode, type in $how.\n{dash:-^50}'''


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

list_hello = ["hello", "hi", "hey", "hola", "Hello", "Hi", "Hey", "Hola"]
list_bye = ["see you", "See you", "bye", "Bye", "bye-bye", "Bye-bye"]

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global mode
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith("j!"):
        h_joke = random.choice(["HaHa!\n", "ROFL\n", "LOL\n"])
        categ = random.choice(["neutral", "all"])
        joke = pyjokes.get_joke(language="en", category=categ)
        await message.channel.send(f"{h_joke}{joke}")

    if msg.startswith("MODE "):
        mode = msg.split("MODE ", 1)[1]

    while(mode == "howto"):
        await message.channel.send(f"You are now in {mode} mode.\n{dash:-^50}")
        if message.author == client.user:
            return

        if msg.startswith("j!"):
            h_joke = random.choice(["HaHa!\n", "ROFL\n", "LOL\n"])
            categ = random.choice(["neutral", "twister", "all"])
            joke = pyjokes.get_joke(language="en", category=categ)
            await message.channel.send(f"{h_joke}{joke}")

        if any(word in msg for word in list_hello):
            await message.channel.send(f"Hello, here's what I can do for you :)\n{howto}")
            break
        else:
            break


#####################  create cypher mode #####################
################################################################

# Caesar cypher uses shift property.
# logo to print.
    while mode == "cypher":
        await message.channel.send(f"You are now in {mode} mode.\n{dash:-^50}")
        await message.channel.send(caesarCy_art.logo)
        await message.channel.send(f"{dash:-^100}")
        # defining a function to encode or decode given text by given shift.

        # taking inputs from user and converting to lower case to remove ambiguity.
        if msg.startswith("code "):
            await message.channel.send("encode or decode (choose one):")
        if msg.startswith("do: "):
            Do_what = msg.split("do: ", 1)[1]
            list_data = Do_what.split(":")
            toDo = list_data[0]
            string_in = list_data[1]
            toShift = int(list_data[2])

            # calling the function.
            list_code = coder(string_in, toShift, toDo)
            await message.channel.send(list_code[0])
            await message.channel.send(list_code[1])

        if msg.startswith("$how"):
            await message.channel.send(f"{usage:-^50}\n1.) Type in: code a message\n2.) Type in format ==> do:[whiteSpace][encode/decode]:[your message]:[shift amount for Caesar cypher].\n{dash:-^50}")
            break

        if msg.startswith("MODE "):
            mode = msg.split("MODE ", 1)[1]
            # await message.channel.send(f"You are now in {mode} mode.")
            break

        else:
            break

        # Remarks: ONLY TEXT(alphabet) IS CODED, example: hello123! with shift 5 is mjqqt123! .


#################################################################

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

####################    create weather mode     ##################
##############  FOR WEATHER FUNCTIONALITIES ######################

    # See what the bot can do.
    while(mode == "weather"):
        await message.channel.send(f"You are now in {mode} mode.\n{dash:-^50}")
        if message.author == client.user:
            return

        if msg.startswith("j!"):
            h_joke = random.choice(["HaHa!\n", "ROFL\n", "LOL\n"])
            categ = random.choice(["neutral", "all"])
            joke = pyjokes.get_joke(language="en", category=categ)
            await message.channel.send(f"{h_joke}{joke}")

        if msg.startswith("$capabilities"):
            cap = "Capabilities"
            await message.channel.send(f"{cap:-^68}\n'$hi' => Show weather of default location,\n'$default' => Show default city,\n'$city [type] [city_name]' => Show weather of certain city,\n'$set [city_name]' => Set default city,\n'$units [CA/KH]' => Set units,\n'$fav [city_name]' => Add city to favorites,\n'$fav $show' => Show favorite cities,\n'$fav $remove [city_name]' => Remove city from favorites,\n'$preferences' => Show default settings.\nNOTE:-\n[type] can be => '$describe' or '$table', set to '$feel' as default.")
            break

        # check default settings.

        if msg.startswith("$preferences"):
            await message.channel.send(f'Default city set as: {db["defCity"]}.')
            if db["units"] == "CA":
                await message.channel.send("Units set as: celsius and atm.")
            elif db["units"] == "KH":
                await message.channel.send("Units set as: kelvin and hPa.")
            break

        # say hello to your bot, gives weather of default city.

        if msg.startswith("$hi"):
            await message.channel.send("Hey there!")
            city_name = db["defCity"]
            weather = wf.get_weather(city_name)
            await message.channel.send(weather)
            break

        # change unit preferences in DB.

        if msg.startswith("$units"):
            unit = msg.split("$units ", 1)[1]
            # units changed to kelvin and hPa.
            if unit == "KH" or unit == "CA":
                db["units"] = unit
                await message.channel.send(f"Unit Preferences Updated To {unit}.")
            else:
                await message.channel.send("I didn't quite get that........")
            break

        # see and manipulate a list of favorite cities in DB.

        if msg.startswith("$fav"):
            fav_city = msg.split("$fav ", 1)[1]

            # remove a favorite city from DB.

            if len(fav_city.split()) > 1:
                if fav_city.split()[0] == "$remove":
                    favorites = db["fav"]

                    if fav_city.split("$remove ", 1)[1] in favorites:
                        to_remove = favorites.index(
                            fav_city.split("$remove ", 1)[1])
                        city_remove = favorites[to_remove]
                        del favorites[favorites.index(
                            fav_city.split("$remove ", 1)[1])]
                        db["fav"] = favorites
                        await message.channel.send(f"Removed {city_remove} From favorites.")
                        break
                    else:
                        await message.channel.send("City Not In favorites.")
                        break

            # show favorite cities in DB.

            elif fav_city == "$show":
                await message.channel.send("Your favorites:")
                if len(db["fav"]) != 0:
                    for f in db["fav"]:
                        await message.channel.send(f)
                    break
                else:
                    await message.channel.send("No favorites Yet.")
                    break

            # add a favorite city to DB.

            else:
                db["fav"].append(fav_city)
                await message.channel.send(f"New favorite {fav_city} Added.")
                break

        # set another city as default.

        if msg.startswith("$set"):
            city_default = msg.split("$set ", 1)[1]
            db["defCity"] = city_default
            await message.channel.send(f"New Default Set As: {city_default}.")
            break

        # see default city set currently.

        if msg.startswith("$default"):
            await message.channel.send(f'Current Location Set As: {db["defCity"]}')
            break

        # check weather of a city.

        if msg.startswith("$city"):
            city_name = msg.split("$city ", 1)[1]
            t = city_name.split()[0]
            if t == "$table":
                weather = wf.get_weather(
                    city_name.split("$table ", 1)[1], "$table")
            elif t == "$describe":
                weather = wf.get_weather(city_name.split(
                    "$describe ", 1)[1], "$describe")
            else:
                weather = wf.get_weather(city_name)
            await message.channel.send(weather)
            break

        if msg.startswith("MODE "):
            mode = msg.split("MODE ", 1)[1]
            # await message.channel.send(f"You are now in {mode} mode.")
            break

        else:
            break


#####################   create song suggestion mode ##########################

    while(mode == "suggest"):
        await message.channel.send(f"You are now in {mode} mode.\n{dash:-^50}")
        # Some global variables.
        global song_name, search_in, num_to_suggest, my_song_name, my_song_pop, my_artist_uri, my_artist_info, my_artist_name, my_artist_pop, my_artist_genres, my_album_name

        if message.author == client.user:
            return

        if msg.startswith("j!"):
            h_joke = random.choice(["HaHa!\n", "ROFL\n", "LOL\n"])
            categ = random.choice(["neutral", "all"])
            joke = pyjokes.get_joke(language="en", category=categ)
            await message.channel.send(f"{h_joke}{joke}")

        if (any(word in msg for word in list_hello)) and ("song: " not in msg):
            await message.channel.send(f"{random.choice(list_hello).title()} there! Tell me a song you like.")
            break

        if (msg.startswith("song: ")) or (msg.startswith("Song: ")):
            if msg.startswith("song: "):
                song_name = msg.split("song: ", 1)[1]
            else:
                song_name = msg.split("Song: ", 1)[1]
            await message.channel.send(f"So you like {song_name},\nLet me see what I can find out about it......")

            # 'results' contains best match to song_name when searched on spotify. [limit = 1]
            # If limit > 1, the data used to identify taste in music would be of the last song from results,
            # That would not be the best match.
            results = sp.search(q='track: ' + song_name,
                                limit=1, offset=0, type='track')
            tracks = results['tracks']['items']
            # However, in this situation, 'tracks' stores data of just one song.

            j = 1
            dict_info = {}
            for track in tracks:
                my_song_name = track['name']
                my_song_pop = track['popularity']

                my_artist_uri = track['artists'][0]['uri']
                my_artist_info = sp.artist(my_artist_uri)
                my_artist_name = track['artists'][0]['name']
                my_artist_pop = my_artist_info['popularity']
                my_artist_genres = my_artist_info['genres']

                my_album_name = track['album']['name']

                sub_dict_info = {"Song Name": my_song_name, "Song Popularity": my_song_pop, "Album": my_album_name,
                                 "Artist Name": my_artist_name, "Artist Popularity": my_artist_pop, "Genres": my_artist_genres}
                dict_info[j] = sub_dict_info

                phrase = "You Like"
                to_send_song_details = f"{phrase:-^50}\n"

                for key in dict_info:
                    for k1 in dict_info[key]:
                        to_send_song_details += "\n"
                        to_send_song_details += f"{k1} --> {dict_info[key][k1]}"

                to_send_song_details += f"\n{dash:-^50}"
                await message.channel.send(to_send_song_details)

            await message.channel.send("Now that that's done, would you like to look for newer songs matching your taste?")
            break

        if msg.startswith("$use"):
            await message.channel.send(f"{usage:-^50}\n1.) Say hello to me!\n2.) Type in a song you like as --> song: [song name]\n3.) Type in a category to search in as --> search: [category]\n\tThe categories available are:\n\ta.) top 50\n\tb.) india\n\tc.) usa\n\td.) uk\n\te.) pop\n\tf.) rock\n\t(These are case-sensitive)\n4.) Now type in the number of songs you want to find that match your taste as --> suggest: [integer]\n{dash:-^50}")
            break

        if (msg.startswith("search: ")) or (msg.startswith("Search: ")):
            if msg.startswith("search: "):
                search_in = (msg.split("search: ", 1)[1]).lower()
            else:
                search_in = (msg.split("Search: ", 1)[1]).lower()
            await message.channel.send(f"How many songs would you like me to try and find for you in {search_in}?")
            break

        if (msg.startswith("suggest: ")) or (msg.startswith("Suggest: ")):
            if msg.startswith("suggest: "):
                num_to_suggest = int(msg.split("suggest: ", 1)[1])
            else:
                num_to_suggest = int(msg.split("Suggest: ", 1)[1])

            await message.channel.send(f"Alright! Finding {num_to_suggest} songs for you in {search_in}.......\n{dash:-^50}")

            # by default search in usa top 50.
            playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbLp5XoPON0wI?si=acd09085445043b7"

            if search_in == "top 50":
                # global top 50 daily.
                playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=7f5d604a0cc24db0"
            elif search_in == "india":
                playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbMWDif5SCBJq?si=86ea3467052645fa"
            elif search_in == "uk":
                playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbMwmF30ppw50?si=661f0af6c2d844a0"
            elif search_in == "usa":
                playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbLp5XoPON0wI?si=acd09085445043b7"
            elif search_in == "pop":
                playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DXbYM3nMM0oPk?si=05e5f56ccba64ff6"
            elif search_in == "rock":
                playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=9636ce06dcb94aae"

            playlist_URI = playlist_link.split("/")[-1].split("?")[0]
            # track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

        # list_to_suggest = []

            i = 1
            for track in sp.playlist_tracks(playlist_URI)["items"]:
                if(i <= num_to_suggest):
                    # track_uri = track["track"]["uri"]
                    track_name = track["track"]["name"]
                    artist_uri = track["track"]["artists"][0]["uri"]
                    artist_info = sp.artist(artist_uri)
                    artist_name = track["track"]["artists"][0]["name"]
                    # artist_pop = artist_info["popularity"]
                    artist_genres = artist_info["genres"]
                    album = track["track"]["album"]["name"]
                    # track_pop = track["track"]["popularity"]

                    if len(artist_genres) != 0:
                        if track_name != my_song_name:
                            flag_match = False
                            for i1 in my_artist_genres:
                                for i2 in artist_genres:
                                    if i1 == i2:
                                        flag_match = True
                            if flag_match == True:
                                await message.channel.send(f"{i}.) Listen to: {track_name} by {artist_name}, from {album}.\n")
                                i += 1
                    else:
                        if (artist_name == my_artist_name) and (track_name != my_song_name):
                            await message.channel.send(f"{i}.) Listen to: {track_name} by the same artist, {artist_name}.\n")
                            i += 1

                        # if (my_song_pop in range(track_pop - 5, track_pop + 10)) and (track_name != my_song_name):
                        #     await message.channel.send(f"{i}.) Listen to: {track_name} by {artist_name}, from {album}.\n")
                        #     i += 1

                        elif (album == my_album_name) and (track_name != my_song_name):
                            await message.channel.send(f"{i}.) Listen to: {track_name} from the same album, {my_album_name}.\n")
                            i += 1
            break

        if any(word in msg for word in list_bye):
            await message.channel.send("See you later, Rock on!")
            break

        if msg.startswith("MODE "):
            mode = msg.split("MODE ", 1)[1]
            # await message.channel.send(f"You are now in {mode} mode.")
            break

        else:
            break


keep_alive()
client.run(TOKEN)

# Next: 1.) ==> Documentation and comments.
