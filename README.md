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

In the early stages of our project we displayed our data via scatter plots. However these plots were susceptible to oversaturation of information which made it impossible to distinguish the magnitude and density of data clusters relative to one another.

We moved from these plots onto heat maps using a package called seaborn. This created much more attractive, and more interesting maps of the data; however, we realized that plots for most players looked very similar. This led us to understand the difference between plotting an individual's raw data vs. plotting that individuals difference from the league. On their own everyone is more successful closer to the net, because it’s a higher likelihood shot. The real interesting information comes when you can see how much better or worse than average an individual player is at certain spots on the court.

Having learned this, we knew we needed a plotting tool that had more customizability than seaborn. We switched to bokeh hex maps because it gave us the ability to manipulate our dataset and give the desired weights for the coloring. Now the really good players stand apart from the rest and you can really see the difference when comparing their plots.


## Demo Video

[NARATED DEMO VIDEO](https://www.youtube.com/watch?v=yQ2LuFMj8M4&feature=youtu.be)

## To Install, before use

* Clone this repository onto your local machine
* $pip install -r Requirements.txt
  * Requirements.txt can be found in the BeforeUse folder

## How to Run

* Download PlayerData2 and TeamData2 from this [link](https://drive.google.com/drive/folders/1GbswBgChzBKQoBmv7sv0RqX9-l3cJXR0?usp=sharing) (this is necessary because each folder was too large to store on github)
  * Keep this cloned repo, PlayerData2, and TeamData2 all in separate folders in the same directory for the tool to work (see below)
  * File structure:
	Main Directory	
	|	
	+--\[FinalSoftDesProject](https://github.com/mayacalabria/FinalSoftDesProject)
	|
	+--\PlayerData2
	|
	+--\TeamData2
  * Make sure to copy both PlayerData2 and TeamData2
  * Keep the folders named PlayerData2 and TeamData2 otherwise the file paths will not be correct

* Navigate to the main directory, where the files GUI.py and main.py are located

* In the comand line run:
  * $ bokeh serve GUI.py \-\-allow-websocket-origin=127.0.0.1:5000
  * (Make sure there are two dashes with no space before allow.)
  * Open a new terminal

* In the new terminal navigate to the main directory again and run:
  * $ python main.py

* Open the link shown in the terminal in your browser of choice

* Enjoy!

## For all Documentation
 * Navigate to main project directory
 * $firefox _build/html/index.html
