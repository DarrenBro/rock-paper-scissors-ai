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


# model = load_model("example-rps-model-1.h5")
# model = load_model("rps-model-1.h5")
# model = load_model("rps-model-2.h5")
# Model 3 best so far
model = load_model("rps-model-3.h5")
# model = load_model("rps-model-4.h5")

# worst
# model = load_model("rps-model-1-mean.h5")

cap = cv2.VideoCapture(0)
previous_move = None

user_current_winner = False

round_count = 0
user_win_count = 0
janken_win_count = 0

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

    # determine winner
    if previous_move != user_move_option:
        if user_move_option != "none":
            # rules to pick the winning move
            janken_win_move = calculate_win_move(user_move_option)
            winner = determine_winner(user_move_option, janken_win_move)

            # round_count += 1
            # if winner == "Janken":
            #     janken_win_count += 1
            # elif winner == "User":
            #     user_win_count += 1

        else:
            janken_win_move = "none"
            winner = "Show me your move"
    previous_move = user_move_option

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_option,
                (110, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Janken's Move: " + janken_win_move,
                (835, 60), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Debugger
    # cv2.putText(frame, "Round count: " + str(round_count), (100, 450), font, 1, (255, 255, 255), 1,cv2.LINE_AA)
    # cv2.putText(frame, "Janken win count: " + str(janken_win_count), (100, 480), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(frame, "User win count: " + str(user_win_count), (100, 510), font, 1, (255, 255, 255), 1,cv2.LINE_AA)
    # cv2.putText(frame, "User current winner: " + str(user_current_winner), (100, 540), font, 1, (255, 255, 255), 1,cv2.LINE_AA)

    try:
        winner
    except NameError:
        print("well, winner WASN'T defined after all!")
    else:
        if janken_win_count == 2:
            cv2.putText(frame, "Janken Wins!", (505, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        elif user_win_count == 2:
            cv2.putText(frame, "User Wins!", (530, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        elif janken_win_count == 2:
            cv2.putText(frame, "Janken Wins!", (5250, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        elif winner == "Show me your move":
            cv2.putText(frame, "Best of 3", (535, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        elif winner == "Janken":
            cv2.putText(frame, "Winner is: " + winner, (470, 600), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

    # set you initial empty results
    icon = cv2.imread("win_images/unknown_win_image.png")
    icon = cv2.resize(icon, (50, 50))

    frame[640:690, 500:550] = icon
    frame[640:690, 600:650] = icon
    frame[640:690, 700:750] = icon

    if round_count == 1:
        if user_current_winner:
            icon = cv2.imread("win_images/user_win_image.png")
        else:
            icon = cv2.imread("win_images/janken_win_image.png")
        icon = cv2.resize(icon, (50, 50))
        frame[640:690, 500:550] = icon

    if round_count == 2:
        if user_current_winner:
            if user_win_count == 1:
                icon = cv2.imread("win_images/user_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 600:650] = icon

                icon = cv2.imread("win_images/janken_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 500:550] = icon

            elif user_win_count == 2:
                icon = cv2.imread("win_images/user_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 500:550] = icon
                frame[640:690, 600:650] = icon
        else:
            if user_win_count == 1:
                icon = cv2.imread("win_images/user_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 500:550] = icon

                icon = cv2.imread("win_images/janken_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 600:650] = icon

            elif user_win_count == 0:
                icon = cv2.imread("win_images/janken_win_image.png")
                icon = cv2.resize(icon, (50, 50))
                frame[640:690, 500:550] = icon
                frame[640:690, 600:650] = icon

    if round_count == 3:
        if user_current_winner:
            icon = cv2.imread("win_images/user_win_image.png")
            icon = cv2.resize(icon, (50, 50))
            frame[640:690, 700:750] = icon
        else:
            icon = cv2.imread("win_images/janken_win_image.png")
            icon = cv2.resize(icon, (50, 50))
            frame[640:690, 700:750] = icon

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
    cv2.imshow("p:Pause/UnPause Image      u:Add User Win      j:Add Janken Win      r:Restart Game      q:Quit", frame)

    key = cv2.waitKey(10)
    if key == ord('u'):
        if user_win_count == 2 or janken_win_count == 3:
            janken_win_count = 0
            user_win_count = 0
            round_count = 0
        round_count += 1
        user_win_count += 1
        user_current_winner = True

    if key == ord('j'):
        if janken_win_count == 2 or user_win_count == 2:
            janken_win_count = 0
            user_win_count = 0
            round_count = 0
        round_count += 1
        janken_win_count += 1
        user_current_winner = False

    if key == ord('p'):
        cv2.waitKey(-1)  # wait until any key is pressed

    if key == ord('r'):
        round_count = 0
        janken_win_count = 0
        user_win_count = 0

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
