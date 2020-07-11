# start with comp plays random move

# human plays their move

# comp sees images

# based on image and rules for game plays the winning move

# play move by test then maybe by generic image?

# note, what if same move made, reset game or display something like draw

# extra: counter for wins

from keras.models import load_model
import cv2
import numpy as np
from random import choice

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}


def mapper(val):
    return REV_CLASS_MAP[val]


def determine_winner(user_move, janken_move):
    if user_move == "rock":
        if janken_move == "scissors":
            return "User"
        if janken_move == "paper":
            return "Janken"

    if user_move == "paper":
        if janken_move == "rock":
            return "User"
        if janken_move == "scissors":
            return "Janken"

    if user_move == "scissors":
        if janken_move == "paper":
            return "User"
        if janken_move == "rock":
            return "Janken"

    if user_move == janken_move:
        return "Tie"


def calculate_win_move(user_move):
    if user_move == "rock":
        return 'paper'
    elif user_move == "paper":
        return 'scissors'
    else:
        return 'rock'


model = load_model("example-rps-model-1.h5")

cap = cv2.VideoCapture(0)

previous_move = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # box for user move
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # box for Janken move
    cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)

    # extract the region of image within the user rectangle
    roi = frame[100:500, 100:500]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (300, 300))

    # predict the move made
    prediction = model.predict(np.array([img]))
    move_code = np.argmax(prediction[0])
    user_move_option = mapper(move_code)

    # predict winner
    if previous_move != user_move_option:
        if user_move_option != "none":

            # easy mode - choice is a random option
            # janken_win_move = choice(['rock', 'paper', 'scissors'])

            # rules to pick the winning move
            janken_win_move = calculate_win_move(user_move_option)
            winner = determine_winner(user_move_option, janken_win_move)
        else:
            janken_win_move = "none"
            # winner = "Waiting for your move"
            winner = "Show me your move"
    previous_move = user_move_option

    # display details
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_option,
                (50, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Janken's Move: " + janken_win_move,
                (750, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

    try:
        winner
    except NameError:
        print("well, winner WASN'T defined after all!")
    else:
        if winner == "Show me your move":
            cv2.putText(frame, winner,
                        (200, 600), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
        elif winner == "Tie":
            cv2.putText(frame, "We're both winners!",
                        (200, 600), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Winner is: " + winner,
                        (200, 600), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)

    if janken_win_move != "none":
        icon = cv2.imread(
            # "computer_move_images/{}.png".format(computer_move_name))
            "computer_move_funny/{}.png".format(janken_win_move))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon
    else:
        icon = cv2.imread(
            "computer_move_funny/show_me_your_move.png")
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    # Title for panel (Needed for pyGame)
    cv2.imshow("Janken Plays Rock-Paper-Scissors", frame)

    k = cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
