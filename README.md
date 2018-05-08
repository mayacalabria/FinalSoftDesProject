# NBA Shot Data Visualization


###### By Maya Calabria, Bryce Mann, and Juan Carlos del Rio
###### Software Design, Olin College of Engineering, Spring 2018

***

## Project Description
For our final project we created a webapp that allows users to visualize the shot patterns for every team and player in the NBA since 1996.

***
## Code Architecture

![Architecture]

[Architecture]: https://raw.githubusercontent.com/mayacalabria/FinalSoftDesProject/master/ClassMaterials/architecture_final.png "High level system diagram"

## Project Progression

![Progression]

[Progression]: https://raw.githubusercontent.com/mayacalabria/FinalSoftDesProject/master/ClassMaterials/progress.png "Project development over time"

## Demo Video

[NARATED DEMO VIDEO](https://www.youtube.com/watch?v=yQ2LuFMj8M4&feature=youtu.be)

## To Install before use

* $pip install -r Requirements.txt
  * Requirements.txt can be found under /BeforeUse/Requirements.txt

## How to Run

* Download all data to the same directory where the folder containing all the project files are stored
  * Google drive link to access this download is on the way
  * Make sure to copy both Player Data and Team Data
  * Check the the folders are named PlayerData2 and TeamData2 otherwise the file paths will not be correct

* Go to the directory where the scripts are located

* In the comand line run:
  * $ bokeh serve GUI.py '- -'allow-websocket-origin=127.0.0.1:5000

* Then run:
  * $ python main.py

* Open the link shown in the terminal in your browser of choice

* Enjoy!

## For all Documentation
 * Navigate to main project directory
 * $firefox _build/html/index.html
