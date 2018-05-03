"""script to loop through all player data and
build team folders and files"""

import os
import sys
import csv

#define directories for player and team data
player_directory = os.path.abspath(os.path.join(os.getcwd(),'../PlayerData'))
team_directory = os.path.abspath(os.path.join(os.getcwd(),'../TeamData'))

#luc longley: 486
#dennis rodman: 772

#loop through playerdata folders
for folder in os.listdir(player_directory):
    folder = os.path.join(player_directory,folder)
    #loop through year files in playerdata folders
    for file in os.listdir(folder):
        #allow the csv rows to be read as lists
        filepath = open(os.path.join(folder,file),'r')
        csv_f = csv.reader(filepath)
        #skips the header row in the loop while storing it for writing to
        #the new team csvs
        headers = next(csv_f)
        #loop through rows of csv
        for row in csv_f:
            #store the team id
            team_id = row[2]
            team_folder = os.path.join(team_directory,team_id)
            #makes the team folder if it hasn't been made yet
            if not os.path.exists(team_folder):
                os.makedirs(team_folder)
            year_file = os.path.join(team_folder,file)
            #makes the year folder for the team if its not there already
            if not os.path.exists(year_file):
                first_year_file = open(year_file,'w',newline='')
                writer = csv.writer(first_year_file)
                #when the file is made write the headers to the first row
                writer.writerow(headers)
                first_year_file.close()
            add_to_year_file = open(year_file,'a',newline='')
            writer = csv.writer(add_to_year_file)
            writer.writerow(row)
            add_to_year_file.close()
