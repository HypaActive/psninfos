from psnawp_api import PSNAWP
import datetime
import os
from dotenv import load_dotenv
import re
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio

load_dotenv()

psnawp = PSNAWP(os.getenv('NPSSO'))

# This is you on PSN
client = psnawp.me()
search = psnawp.search()

# Initial variables
games_completed = 0
bronze_all = silver_all = gold_all = platinum_all = 0
bronze_earned = silver_earned = gold_earned = platinum_earned = 0
games = 0
current_game_trophy_list = []
current_game_trophy_details = {}
current_game_trophies_all = None

# File to write results to
filepath_100percent = os.getenv('FILEPATH_100PERCENT')
filepath_trophies_current_game = os.getenv('FILEPATH_TROPHIES_CURRENT_GAME')


# Twitch function to get current (when live) or last played game
async def twitchGetGame():
    twitch = await Twitch(os.getenv('TWITCH_APP_ID'), os.getenv('TWITCH_APP_SECRET'))
    user = await first(twitch.get_users(logins=os.getenv('TWITCH_USER'))) # get user details
    global current_game_twitch 
    channel_info = await twitch.get_channel_information(user.id)
    current_game_twitch = channel_info[0].game_name

# run function
asyncio.run(twitchGetGame())

# Get all games and status
all_games = client.trophy_titles(limit=None)

# Get number of games total and details on last played game
for trophy_title in all_games:
    if (trophy_title.progress==100):
        games_completed += 1
    # try to match Twitch game name with PSN game name (e.g. Twitch: Blasphemous II, PSN: Blasphemous 2)
    if (trophy_title.title_name.startswith(current_game_twitch) and current_game_trophies_all == None):
        current_game_trophies_all = trophy_title.defined_trophies.bronze + trophy_title.defined_trophies.silver + trophy_title.defined_trophies.gold + trophy_title.defined_trophies.platinum
        current_game_trophies_earned = trophy_title.earned_trophies.bronze + trophy_title.earned_trophies.silver + trophy_title.earned_trophies.gold + trophy_title.earned_trophies.platinum
    elif (trophy_title.title_name.startswith(re.search(pattern="(\w+)\s?", string=current_game_twitch).group(0)) and current_game_trophies_all == None):
        current_game_trophies_all = trophy_title.defined_trophies.bronze + trophy_title.defined_trophies.silver + trophy_title.defined_trophies.gold + trophy_title.defined_trophies.platinum
        current_game_trophies_earned = trophy_title.earned_trophies.bronze + trophy_title.earned_trophies.silver + trophy_title.earned_trophies.gold + trophy_title.earned_trophies.platinum
    else:
        if (games == 0):
            current_game_np_id = trophy_title.np_communication_id
            for platform in trophy_title.title_platform:
                current_game_platform = platform.value
            current_game_trophies_all = trophy_title.defined_trophies.bronze + trophy_title.defined_trophies.silver + trophy_title.defined_trophies.gold + trophy_title.defined_trophies.platinum
            current_game_trophies_earned = trophy_title.earned_trophies.bronze + trophy_title.earned_trophies.silver + trophy_title.earned_trophies.gold + trophy_title.earned_trophies.platinum
    bronze_all += trophy_title.defined_trophies.bronze
    silver_all += trophy_title.defined_trophies.silver
    gold_all += trophy_title.defined_trophies.gold
    platinum_all += trophy_title.defined_trophies.platinum
    bronze_earned += trophy_title.earned_trophies.bronze
    silver_earned += trophy_title.earned_trophies.silver
    gold_earned += trophy_title.earned_trophies.gold
    platinum_earned += trophy_title.earned_trophies.platinum
    games += 1

# Open files
file_100percent = open(filepath_100percent, "w")
file_trophies_current_game = open(filepath_trophies_current_game, "w")

# Write to files
file_100percent.write("100% PSN Account: " + str('{:.2%}'.format((bronze_earned + silver_earned + gold_earned + platinum_earned) / (bronze_all + silver_all + gold_all + platinum_all))) + " Completion | " + str((bronze_all + silver_all + gold_all + platinum_all) - (bronze_earned + silver_earned + gold_earned + platinum_earned)) + " Unearned Trophies | " + str((games - games_completed)) + " Unfinished Games | ")
file_trophies_current_game.write(str('{:02d}'.format(current_game_trophies_earned)) + "/" + str(current_game_trophies_all) + " Trophies")

# Close files
file_100percent.close()
file_trophies_current_game.close()