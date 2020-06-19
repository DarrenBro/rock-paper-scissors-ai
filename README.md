# rock-paper-scissors-ai
AI Bot to play rock-paper-scissors against a human

# tensorflow-python
Code Engine: Image Classifier with 3 categories (rock, paper, scissors)
SqueezeNet will be our pre-trained CNN, and we'll re-train its output layers for our 3 new categories.

# 5 Steps we'll generally follow to create this ai
1. Collecting data - gathering images from our own webcam
2. Creating a Neural Network
3. Training the model
4. Test the model
5. Deploy model into a web app or soemthing to only it to easily play users.

# Step 0 - Setup
1. git clone / download this project
2. Create a virtual environment (recommended for python, I'm using python3) run in terminal "python3 -m venv ."
3. run "source bin/activate" you should need your root inserted to your terminal.
4. having pip installed in useful for the next part "easy_install pip"
5. there is a dependency_list.txt, you can install them with pip run "pip install -r dependency_list.txt"

# Step 1 - Gathering images
1. script to run first is "collect_image_data.py"
2. Run command example: python collect_image_data.py rock 200
3. Press 's' to start/pause and q to quit.
4. Images stored in 'collected_images' dir with label set as 1st argument
