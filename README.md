# AI-sign-recognition
Project done for subject Artificial Intelligence Fundamentals.

Project is a model of CNN for german signs recognition.

It was deployed on anvil. Now doesn't work, but you can make your own anvil project and just connect it.

# Dataset:
Dataset is available here:

https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign

It was used for training and testing.

# Files:
1. Presentation.pdf is a summary of a project.
2. classes - simple json file containing a dictionary <number,sign name> for loops in modelling.
3. App.py - loading saved model and establishes connection to anvil
4. my_model.h5 - model of CNN
5. ModellingModel.py - pre-processing, loading data and modelling the model
6. process.sh - installing necessary libraries and runs scripts
