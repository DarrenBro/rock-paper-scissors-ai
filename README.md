# The rock-paper-scissors AI: "janken"
AI Bot to play rock-paper-scissors against a human

# Medium Article
https://towardsdatascience.com/rock-paper-scissors-ai-bot-janken-ee2d3089b778

# Why the name janken?
Rock Paper Scissors was first introduced by China during the 17th century, it was called Janken.

# Language:python Libraries: Keras/OpenCV/Numpy
1. Code Engine: Image Classifier with 3 categories (rock, paper, scissors)
2. SqueezeNet will be our pre-trained CNN 
3. We'll re-train its output layers for our 3 new categories

# Steps we'll generally follow to create this ai
1. Collecting data - gathering images from your own web camera
2. Creating a Neural Network & Training the model
3. Test the model
4. Play the game!

# Step 0 - Setup
1. git clone / download this project
Create a virtual environment (recommended for python, I'm using python3) 
Your pyCharm or chosen IDE might offer (venv) on new a project.
You can run source venv/bin/activate if it comes pre-setup, if not, here are the steps.
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
1. Add a dir folder in root called "collected_images"
2. In this dir add 4 more folders like so; 
![image](https://user-images.githubusercontent.com/8710774/110144959-d713ca00-7dd0-11eb-854b-e90e3d1e150e.png)
3.  script to run first is "collect_image_data.py"
4. Run command example: "python collect_image_data.py rock 200"
5. Press 's' to start/pause and q to quit.
6. Images stored in 'collected_images' dir with label set as 1st argument

# Step 2 - Training Neural Network
* You can skip all of step 2 if you just want to test a model, I've provided the necessary file.
1. The training part is all in "train_model.py" and the squeeze-net model weights .h5 files.
2. Script to run first is "python train_model.py"
3. Training time for a batch of (200 images across 4 categories) should be less than 10 minutes.
4. When finished will produce a model file called "rps-model-1.h5" in project root.
5. You will also see something like 

Epoch 10/10
1200/1200 [==============================] - 74s 62ms/step - loss: 4.4444e-05 - acc: 1.0000

Two important figures to look at is 'loss' and 'acc'.
This is showing us the loss is an extremely low value and the accuracy is 100%
For now just note that both of these ranges are extremely desired and if you get 
something similar, this will be enough to test out.

# Step 3 - Testing the Model
1. You can use your model or the example one I've provided, "example-rps-model-1.h5".

2. This file contains all the training parameter, weights and biases which the NN learnt.
3. Change model name if you have trained a new model (line with comment "# Change for your model name")
3. I've provided test images in "test_images" dir.
4. Make sure when you run the below command you include the extension .jpg
4. Script to test model is "test_model.py", run for any image e.g. "python test_model.py test_images/paper.jpg".
6. Script will print string prediction at end like "Predicted the image is: paper".

# Step 4 - Play the game
1. Script to run is "python play.py".
2. Place your gesture in user box and test it out.
3. p:Pause/UnPause Image    
4. u:Add User Win
5. j:Add Janken Win
6. r:Restart Game
7. q:Quit

# Further Improvement Ideas
1. A running server to run the game to allow easier playing and no script running necessary.

2. rock paper scissors lizard spock
The rules: "Scissors decapitate Scissors cuts paper, paper covers rock, rock crushes lizard, 
lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard, lizard eats paper, 
paper disproves Spock, Spock vaporizes rock, and as it always has, rock crushes scissors."

3. Evaluation (reported testing) during model training.
4. Tensor board setup (Only put in as a dependency for now)
5. Score counter for unlimited gaming but more useful to see if Janken gets 9/10 or 99/100 wins.
6. Feature focus and black and white imaging only for training and for game running.
7. Introduce more hyper parameters and tweak existing ones (to optimise training).



