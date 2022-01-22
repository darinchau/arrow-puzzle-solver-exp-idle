This script solves the exponential idle hard arrow puzzle. It hasn't been very well tested yet but oh well

I decided to share this script because why not.

Instructions:

0. Get the required packages: You need python 3.6 or above (I use 3.9)
Pure python adb for reading and sending phone data: pip install -U pure-python-adb
Pillow for image recognition: pip install pillow
MEmu: the emulator of choice

1. Install exponential idle on your emulator (tested on Android 7.1) and go to the hard arrow puzzle page

2. Connect your emulator to the adb server by running "adb connect 127.0.0.1:21503" on your server

3. Set your emulator resolution to 1200 x 800

4. Set the arrow puzzle settings to greyscale and displaying numbers

5. Run the script. If everything goes well it should solve one board in an average of 6 seconds.