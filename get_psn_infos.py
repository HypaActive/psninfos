from psnawp_api import PSNAWP
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

psnawp = PSNAWP(os.getenv('NPSSO'))

# This is you
client = psnawp.me()
search = psnawp.search()

# Initial variables
games_completed = 0
bronze_all = silver_all = gold_all = platinum_all = 0
bronze_earned = silver_earned = gold_earned = platinum_earned = 0
games = 0
current_game_trophy_list = []
current_game_trophy_details = {}

# File to write results to
filepath_100percent = "C:\\Users\\stein\\100percent.txt"
filepath_trophies_current_game = "C:\\Users\\stein\\trophies.txt"



# Get all games and status
all_games = client.trophy_titles(limit=None)

# Get number of games total and details on last played game
for trophy_title in all_games:
    if (trophy_title.progress==100):
        games_completed += 1
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
file_100percent.write("100% PSN Account: " + str('{:.2%}'.format((bronze_earned + silver_earned + gold_earned + platinum_earned) / (bronze_all + silver_all + gold_all + platinum_all))) + " Completion | " + str((bronze_all + silver_all + gold_all + platinum_all) - (bronze_earned + silver_earned + gold_earned + platinum_earned)) + " Unearned Trophies | " + str((games - games_completed)) + " Unfinished Games")
file_trophies_current_game.write(str('{:02d}'.format(current_game_trophies_earned)) + "/" + str(current_game_trophies_all) + " Trophies")

# Close files
file_100percent.close()
file_trophies_current_game.close()