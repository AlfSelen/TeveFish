Welcome to Fishing macro made by GoriMeri 
History:
Made a fishing macro back in 2019 before Evo mostly for fun, and made a version which worked for Daemonic Sword RPG.
This program have been through serveral rewritings with different ways of solving the problem

Features:
Auto fish - Will detect fishing presses and fish correctly, 90% of the time it works 100% of the time. (Play around with cam distance if the fishing is wrong)
Support for all fishing zones - (0,1,2,3,4) counting from zero, change POSITION in settings.py to your choosing
Death detection - Will detect is hero is dead and move back to your position
Autodrop when full - Will detect if your inventory is to full to fish, and drop your items on your character's feet
Autodrop after timer - Will drop fish every so often, game has a limit of up to 10M gold, and a 100 stack of fish (good quality) would be more than the limit
Final zone pathing - Will run around the elves in the final zone fishing
Auto stuck detection - Will kill the hero if your are stuck for a prolonged time and go to fishing position
Automatic resolution detection - Should work at all screen resolutions.v

Installation easy:
1. install Anaconda (python programming tool) https://www.anaconda.com/
2. Open anaconda prompt
3. Write: conda create --name teve			(This should make a environment for your package)
4. Write: conda activate teve				(This should activate the environment)
5. conda install -c conda-forge tesserocr	(This will install the scanning package)
6. Write: pip install -r requirements.txt	(This will install the other required packages required for the program to run)

Settings setup:
In settings.py change POSITION variable to corresponding number.
0 is 1st fishing spot
1 is 2nd
2 is 3rd
3 is 4th
4 is 5th and last fishing spot (default)

Ingame setup:
1. Hero should be on control group 1 
2. Hero should have set revival point to the clostest to the fishing spot
3. Fishing rod should be in first slot, optional item 2nd slot.


Run the program:
1. open anaconda prompt
	1.1. cd "path with the main.py"
	1.2. conda activate teve
	1.3. python main.py
Then program will start within 3 sec
Shift + P: Pause / Unpause program
Shift + Q: Quit program


Installation hard - if you wanna do it another way
1. Make sure python is installed
2. Install the required libraries: pip install -r requirements.txt and the tesserocr library.
3. Change variable 'tess_path' to your tesserocr path, (write tesseract in cmd, might help ya)




Version 1.1:
New: Automatic resolution detection added - This means that the software should work at all screen resolutions.
Version 1.1a:
Fixed small bug with last fishing spot not working with all screen resolutions

Copyright GoriMeri, your hereby agree that you will not share the program with others without my consent.