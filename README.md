# NBA Shot Data Visualization


###### By Maya Calabria, Bryce Mann, and Juan Carlos del Rio
###### Software Design, Olin College of Engineering, Spring 2018

***

## Project Description
For our final project we created a web app that allows users to visualize the shot patterns for every team and player in the NBA since 1996. There is an immense amount of sports data online nowadays, but it can be hard to parse, and challenging to access. We have created an interactive data visualization tool for basketball fans. Our heat maps allow the user to see how players and teams compare to league averages in both frequency and
accuracy of shots taken.

***
## Code Architecture

![Architecture]

[Architecture]: https://raw.githubusercontent.com/mayacalabria/FinalSoftDesProject/master/ClassMaterials/architecture_final.png "High level system diagram"

Let’s break down the structure of our code. First we started with data collection. We had a script that scraped all relevant data from the NBA website. Then we sorted that data into a system of folders that grouped it either by player or by team and stored a csv of shot data for each season. We did this for more than 1500 players and about 30 teams, which is approximately 11,000 individual seasons of data.

After acquiring this data, we created a function to calculate the difference between each player’s shooting accuracy and the leagues average by zone. We repeated this process for shooting frequency, and adapted both functions to calculate the same information for teams. We then created classes for both Team and Player that when instantiated, pull the required data for an individual or team, and display the calculated difference from league data as a hex plot.

We used Bokeh, a visualization tool to make our plots and create the accompanying interactivity. The widget allows user to select what group of data they want to visualize, what filters to put on it, and who they want to look at using user callbacks that update the arguments passed to our Player and Team classes. From here we rendered the widget to a web browser using flask.


## Project Progression

![Progression]

[Progression]: https://raw.githubusercontent.com/mayacalabria/FinalSoftDesProject/master/ClassMaterials/progress.png "Project development over time"

## Demo Video

[NARATED DEMO VIDEO](https://www.youtube.com/watch?v=yQ2LuFMj8M4&feature=youtu.be)

## To Install before use

* $pip install -r Requirements.txt
  * Requirements.txt can be found under in the BeforeUse folder

## How to Run

* Download all data to the same directory where the folder containing all the project files are stored
  * Google drive link to access this download is on the way
  * Make sure to copy both Player Data and Team Data
  * Check the the folders are named PlayerData2 and TeamData2 otherwise the file paths will not be correct

* Go to the directory where the scripts are located

* In the comand line run:
  * $ bokeh serve GUI.py \-\-allow-websocket-origin=127.0.0.1:5000
  * (Make sure there are two dashes with no space before allow.)

* Then run:
  * $ python main.py

* Open the link shown in the terminal in your browser of choice

* Enjoy!

## For all Documentation
 * Navigate to main project directory
 * $firefox _build/html/index.html
