Welcome to Fishing macro made by GoriMeri 
History:
Made a fishing macro back in 2019 before Evo mostly for fun, and made a version which worked for Daemonic Sword RPG.
This program have been through several rewritings with different ways of solving the problem

Features:
Auto fish - Will detect fishing presses and fish correctly
Support for all fishing zones - (0,1,2,3,4) counting from zero, change POSITION in settings.py to your choosing
Death detection - Will detect is hero is dead and move back to your position
Auto drop when full - Will detect if your inventory is to full to fish, and drop your items on your character's feet
Auto drop after timer - Will drop fish every so often, game has a limit of up to 10M gold, and a 100 stack of fish (good quality) would be more than the limit
Final zone pathing - Will run around the elves in the final zone fishing
Auto stuck detection - Will kill the hero if your are stuck for a prolonged time and go to fishing position
Automatic resolution detection - Should work at all screen resolutions.

Installation:
- Make sure to have python installed on your computer (https://www.python.org/)
- Run install.bat (double click on it in the folder)

Settings setup:
In settings.py change POSITION variable to corresponding number.
0 is 1st fishing spot
1 is 2nd
2 is 3rd
3 is 4th
4 is 5th and last fishing spot (default)

Ingame setup:
1. Hero should be on control group 1 
2. Hero should have set revival point to the closest to the fishing spot
3. Fishing rod should be in first slot, rest should be empty, except when at 4th fishing spot where you may bring an item in the 2nd spot
4. There should be no items in 5th and 6th item spot when starting the program


Run the program:
- Run run.bat (you can run it by double clicking on it in the folder)
Then program will start within 3 sec
Shift + P: Pause / Unpause program
Shift + Q: Quit program


Version 1.1:
New: Automatic resolution detection added - This means that the software should work at all screen resolutions.
Version 1.1a:
Fixed small bug with last fishing spot not working with all screen resolutions
Version 2.0
Reduced the complexity, reduced the dependencies, installation process made easier and patched the program to work with the new version on wc3 (the fonts were tweaked in a update which broke the detection).
Also moved project to Github.
Version 2.0.1
Fixed detection of arrow presses, should now work on all resolutions
Version 2.0.1a
Fixed first fishingspot
Version 3.0.0
Runs more smoothly, install is now only one click

Good luck and enjoy!
