from keras.models import load_model
import cv2
import numpy as np

INDEX_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}


def mapper(value):
    return INDEX_MAP[value]


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
    # "frame" will get the next frame in the camera
    # "frame" is an image array vector captured based on the default frames per second defined explicitly or implicitly
    # "ret" will obtain return value from getting the camera frame, either true of false.
    # "cap" is a VideoCapture object
    ret, frame = cap.read()
    if not ret:
        continue

    # box for user move
    # frame - on which rectangle is to be drawn
    # (100, 100) - starting coordinates of rectangle, x-coord & y-coord
    # (420, 420) - end coordinates
    # (255, 255, 255) - white colour
    cv2.rectangle(frame, (100, 100), (420, 420), (255, 255, 255))
    # user_image = frame[100:420, 100:420]

    # box for Janken move
    # to make a square difference between coordinates must be the same (800 - 100) = (1200 - 500) e.g. 700
    cv2.rectangle(frame, (800, 100), (1200, 500), (0, 0, 0))

    # box for win counters
    cv2.rectangle(frame, (500, 640), (550, 690), (0, 0, 0))
    cv2.rectangle(frame, (600, 640), (650, 690), (0, 0, 0))
    cv2.rectangle(frame, (700, 640), (750, 690), (0, 0, 0))

    # capture frame image of user's move
    user_image = frame[100:420, 100:420]
    image = cv2.cvtColor(user_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 300))

    # predict the move made
    prediction = model.predict(np.array([image]))
    move_code = np.argmax(prediction[0])
    user_move_option = mapper(move_code)

    round_count = 0
    janken_win_count = 0
    user_win_count = 0

    # determine winner
    if previous_move != user_move_option:
        if user_move_option != "none":
            # rules to pick the winning move
            janken_win_move = calculate_win_move(user_move_option)
            winner = determine_winner(user_move_option, janken_win_move)
            round_count += 1

            if winner == "Janken":
                janken_win_count += 1
            elif winner == "User":
                user_win_count += 1

        else:
            janken_win_move = "none"
            winner = "Show me your move"
    previous_move = user_move_option

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_option,
                (110, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Janken's Move: " + janken_win_move,
                (835, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # icon = cv2.imread("win_images/unknown_win_image.png")
    # icon = cv2.resize(icon, (50, 50))
    # frame[600:650, 600:650] = icon

    # icon = cv2.imread("win_images/janken_win_image.png")
    # icon = cv2.resize(icon, (50, 50))
    # frame[600:650, 600:650] = icon
    #
    # icon = cv2.imread("win_images/user_win_image.png")
    # icon = cv2.resize(icon, (50, 50))
    # frame[600:650, 600:650] = icon

    try:
        winner
    except NameError:
        print("well, winner WASN'T defined after all!")
    else:
        if round_count == 0:
            cv2.putText(frame, "Best of 3",
                        (550, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        elif winner == "Tie":
            cv2.putText(frame, "We're both winners!",
                        (550, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Winner is: " + winner,
                        (470, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

    if janken_win_move != "none":
        icon = cv2.imread(
            # "computer_move_images/{}.png".format(computer_move_name))
            "computer_move_funny/{}.png".format(janken_win_move))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon
    else:
        icon = cv2.imread("computer_move_funny/show_me_your_move.png")
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    # Title for panel (Needed for pyGame)
    cv2.imshow("Place Hand Gesture In Empty Box", frame)

    k = cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
