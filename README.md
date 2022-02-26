# Arrow puzzle solver

This script solves the exponential idle hard arrow puzzle. This program is distributed AS IS. If there is an error, please raise it in the issues page.

Instructions:

0. Get the required packages: You need python 3.6 or above (I use 3.9)
Pure python adb for reading and sending phone data: pip install -U pure-python-adb
Pillow for image recognition: pip install pillow
MEmu: the emulator of choice

Also, we assume you have ee5000+. Otherwise, you can uncomment "pass" under CheckTheories() in main.py

1. Your exponential idle must be on dark mode, English

2. Connect your emulator to the adb server by running "adb connect 127.0.0.1:21503" on your server

3. Set your emulator resolution to 1200 x 800 and CPU settings to the highest as long as it doesn't interfere your daily work

4. Set the arrow puzzle settings to greyscale and displaying numbers

5. Run the script. If everything goes well it should solve on it's own.

There are some extra functions in case you are interested; however they require extra setup

# Other functionalities

1. Auto-acceleration: If you have some auto clicker installed please have it spam somewhere about one quarter of down the top of the screen, and have its play button a bit below the accel button (on top). It should auto hold accel for you

2. Auto T5: Install tesseract from https://github.com/UB-Mannheim/tesseract/wiki and pytesseract from "pip install pytesseract". Then somewhere around line 17 in theories.py, put the directory of tesseract.exe into the variable. A sample has been done for you.

If you do not want these functionalities, please delete the line somewhere in the bottom of main.py where it says t1.start(). Otherwise, if it doesn't work for you, please download an older commit


=================================================================================================================


Update: I decided to remove everything except the basic functionalities so that the user could get an experience as smooth as possible

Statistics: (10000 solves) Average = 5.543 real time seconds, Standard deviation = 1.092, Fastest time = 1.588