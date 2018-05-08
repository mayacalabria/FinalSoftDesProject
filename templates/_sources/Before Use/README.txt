.. _README:

*****************
NDV Read ME File
*****************

**By Maya Calabria, Bryce Mann, and Juan Carlos del Rio**
**Software Design, Olin College of Engineering, Spring 2018**


Demo Video
==========

`NARATED DEMO VIDEO <https://www.youtube.com/watch?v=yQ2LuFMj8M4&feature=youtu.be>`_

Project Description
===================

For our final project we created a webapp that allows users to visualize the shot patterns for every team and player in the NBA since 1996.

To Install before use
=====================

* $pip install -r requirements.txt
    * requirements.txt can be found under /Before Use/requirements.txt

How to Run
==========

* Download all data to the same directory where the folder containing all the project files are stored

     * Make sure to copy both Player Data and Team Data

     * Check the the folders are named PlayerData2 and TeamData2 otherwise you will run into 'Key error: ZONE FREQUENCY'

* Go to the directory where the scripts are located

* In the command line run:

    * $ bokeh serve GUI.py --allow-websocket-origin=127.0.0.1:5000


* Then run:
    * $ python main.py


* Open the link shown in the terminal in your browser of choice

* Enjoy!
