# rock-paper-scissors-ai
AI Bot to play rock-paper-scissors against a human

# Language:python Libraries: Keras/OpenCV/Numpy
1. Code Engine: Image Classifier with 3 categories (rock, paper, scissors)
2. SqueezeNet will be our pre-trained CNN 
3. We'll re-train its output layers for our 3 new categories

# 5 Steps we'll generally follow to create this ai
1. Collecting data - gathering images from our own web camera
2. Creating a Neural Network
3. Training the model
4. Test the model
5. Deploy model into a web app to easily let users plays.

# Step 0 - Setup
1. git clone / download this project
Create a virtual environment (recommended for python, I'm using python3) 
2. run in terminal "python3 -m venv ." (there's a space after the last 'v'). This will create
a bin folder in root with an activate script for a virtual env.

3. If you get error like "Unable to symlink" delete the bin folder that was created in root and try again. Didn't work? 
Try checking your path from python "which python3" or $PATH in bash_profile "echo $PATH" or "open .bash_profile".
For example, here is my path export PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:$PATH"

4. run "source bin/activate" from folder root. Should prefix your folder name in brackets.
5. "python -V" should return Python 3 or >
6. Install pip3 "brew install python3" (pip3 is auto installed with this command)
7. There is a dependency_list.txt, run "pip3 install -r dependency_list.txt"

# Step 1 - Gathering images
1. script to run first is "collect_image_data.py"

2. Run command example: python collect_image_data.py rock 200
3. Press 's' to start/pause and q to quit.
4. Images stored in 'collected_images' dir with label set as 1st argument
