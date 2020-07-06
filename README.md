# rock-paper-scissors-ai
AI Bot to play rock-paper-scissors against a human

# Language:python Libraries: Keras/OpenCV/Numpy
1. Code Engine: Image Classifier with 3 categories (rock, paper, scissors)
2. SqueezeNet will be our pre-trained CNN 
3. We'll re-train its output layers for our 3 new categories

# Steps we'll generally follow to create this ai
1. Collecting data - gathering images from our own web camera
2. Creating a Neural Network & Training the model
3. Test the model
4. Deploy model into a web app to easily let users plays.

# Step 0 - Setup
1. git clone / download this project
Create a virtual environment (recommended for python, I'm using python3) 
Your pyCharm or chosen IDE might offer this on new a project, if not, here are the steps.
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
2. script to run first is "collect_image_data.py"

3. Run command example: "python collect_image_data.py rock 200"
4. Press 's' to start/pause and q to quit.
5. Images stored in 'collected_images' dir with label set as 1st argument

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

# Step 3 - Running the Model
1. You can use your model or the example one I've provided, "example-rps-model-1.h5".
2. This file contains all the training parameter, weights and biases which the NN learnt.
3. Script to test model is "test_model.py", run "python test_model.py".
As far as I've got.







