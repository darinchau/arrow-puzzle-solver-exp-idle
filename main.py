# pip install -U pure-python-adb
# pip install pillow
from ppadb.client import Client
from PIL import Image
import numpy as np
import time
from subprocess import call

#Number of boards solved
i = 0
DEBUG_MESSAGES = False

# 1. Connect to device
client = Client(host='127.0.0.1', port=5037)
devices = client.devices()

if len(devices) == 0:
    raise RuntimeError("No devices connected")

device = devices[0]


def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)


def sendClick(imgCoords: tuple):
    if DEBUG_MESSAGES:
        print(f"Clicking {imgCoords}")
    call(["adb", "shell", "input", "tap", str(imgCoords[1]), str(imgCoords[0])])


def getState(imgCoord: tuple):
    if (imgCoord[0] < 0):
        return 0

    pixel = Img[imgCoord[0]][imgCoord[1]]
    # assert pixel[0] == 17 or pixel[0] == 85
    if pixel[0] < 20:
        return 1
    return 2


def getImgCoord(localCoord: tuple):
    if not isValid(localCoord):
        return (-1, -1)
    return (-50 * localCoord[1] + 720, 85 * localCoord[0] + 400)


def isValid(localCoord: tuple):
    c = abs(localCoord[0]) + abs(localCoord[1])
    return abs(localCoord[0]) < 4 and abs(localCoord[1]) < 7 and c < 7 and c % 2 == 0


def getStateFromBoard(board, localCoords: tuple):
    return board[localCoords[0] + 3][localCoords[1] + 6]


def setStateOnBoard(board, localCoords: tuple):
    grid = board[localCoords[0] + 3][localCoords[1] + 6]
    grid += 1
    if grid == 3:
        grid = 1
    board[localCoords[0] + 3][localCoords[1] + 6] = grid
    return board


def MakeMoveOn(board, localCoords: tuple, click = True):
    # Handle the board, for itself and its 6 neighbours
    for i in [localCoords, (localCoords[0], localCoords[1] + 2), (localCoords[0], localCoords[1] - 2), (localCoords[0] + 1, localCoords[1] + 1), (localCoords[0] + 1, localCoords[1] - 1), (localCoords[0] - 1, localCoords[1] + 1), (localCoords[0] - 1, localCoords[1] - 1)]:
        if isValid(i):
            board = setStateOnBoard(board, i)

    # print(f"Making move on {localCoords}")

    # Handle the device
    if click:
        sendClick(getImgCoord(localCoords))
    return board

# Solve a cell by clicking the one below it

def solveBottom(board, localCoords: tuple, click = True):
    south = (localCoords[0], localCoords[1] - 2)
    # Check if there is a bottom cell
    if isValid(south):
        if getStateFromBoard(board, localCoords) == 2:
            board = MakeMoveOn(board, south, click)
    return board

def copyBoard(board):
    copy = []
    for i in range(len(board)):
        arr = []
        for j in range(len(board[0])):
            arr.append(board[i][j])
        copy.append(arr)
    return copy



def propogate(board, click = True):
    # Doing things the hard way :D
    solveSequence = [(0, 6), (-1, 5), (-2, 4), (-3, 3), (1, 5), (2, 4), (3, 3),
                     (0, 4), (-1, 3), (-2, 2), (-3, 1), (1, 3), (2, 2), (3, 1),
                     (0, 2), (-1, 1), (-2, 0), (-3, -1), (1, 1), (2, 0), (3, -1),
                     (0, 0), (-1, -1), (-2, -2), (1, -1), (2, -2),
                     (0, -2), (-1, -3), (1, -3), (-0, -4)]

    for i in range(len(solveSequence)):
        board = solveBottom(board, solveSequence[i], click)

    return board


def solve(board):
    copy = copyBoard(board)
    copy = propogate(copy, False)
    # print(board[0])
    # print(copy[0])
    solver = (0, 0, 0, 0)
    parity = (getStateFromBoard(copy, (-3, -3)), getStateFromBoard(copy, (-2, -4)),
              getStateFromBoard(copy, (-1, -5)), getStateFromBoard(copy, (0, -6)))
    if parity == (1, 1, 2, 1):
        solver = (0, 1, 0, 0)
    elif parity == (1, 2, 1, 2):
        solver = (0, 1, 1, 0)
    elif parity == (1, 2, 2, 2):
        solver = (0, 0, 1, 0)
    elif parity == (2, 1, 1, 2):
        solver = (1, 0, 0, 0)
    elif parity == (2, 1, 2, 2):
        solver = (0, 0, 0, 1)
    elif parity == (2, 2, 1, 1):
        solver = (0, 0, 1, 1)
    elif parity == (2, 2, 2, 1):
        solver = (1, 0, 1, 0)

    if DEBUG_MESSAGES:
        print(parity)

    if solver[0]:
        board = MakeMoveOn(board, (-3, 3))
    if solver[1]:
        board = MakeMoveOn(board, (-2, 4))
    if solver[2]:
        board = MakeMoveOn(board, (-1, 5))
    if solver[3]:
        board = MakeMoveOn(board, (0, 6))

    board = propogate(board)
    return board


def testClicks():
    for x in range(-3, 4):
        for y in range(-6, 7):
            if isValid((x, y)):
                print(f"Clicking {(x,y)}")
                imgCoord = getImgCoord((x, y))
                sendClick(imgCoord)
                Img[imgCoord[0]][imgCoord[1]] = [255, 0, 0, 255]
    image = Image.fromarray(Img)
    image = image.save("screen.png")


#### The main loop portion ####
while True:
    # 2. Get image
    take_screenshot(device)
    image = Image.open('screen.png')
    Img = np.asarray(image)

    resolution = (len(Img), len(Img[0]))
    # print(resolution)

    # 3. Get board state and store it into an array
    board = []
    for x in range(-3, 4):
        arr = []
        for y in range(-6, 7):
            arr.append(getState(getImgCoord((x, y))))
        board.append(arr)

    board = solve(board)
    sendClick((1120, 360))
    time.sleep(0.5)
    sendClick((69, 648))
    i += 1
    print("solved " + str(i) + " boards")
    time.sleep(0.5)