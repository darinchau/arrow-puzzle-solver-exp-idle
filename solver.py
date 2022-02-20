# pip install -U pure-python-adb
# pip install pillow
from ppadb.client import Client
from PIL import Image
import numpy as np
import time
from subprocess import call
import PySimpleGUI as sg


def initialize():
    # 1. Connect to device
    client = Client(host='127.0.0.1', port=5037)
    devices = client.devices()

    if len(devices) == 0:
        raise RuntimeError("No devices connected")

    time.sleep(2)
    return devices[0]


def take_screenshot(device, imagename):
    image = device.screencap()
    with open(imagename, 'wb') as f:
        f.write(image)


def clickOn(x, y, wait=False):
    call(["adb", "shell", "input", "tap", f"{x}", f"{y}"])
    if wait:
        time.sleep(1.2)


def sendClick(localCoord: tuple):
    imgCoords = (85 * localCoord[0] + 400, -50 * localCoord[1] + 720)
    clickOn(imgCoords[0], imgCoords[1])


def getState(Img, imgCoord: tuple):
    if (imgCoord[0] < 0):
        return 0

    pixel = Img[imgCoord[1]][imgCoord[0]]
    # assert pixel[0] == 17 or pixel[0] == 85
    if pixel[0] < 20:
        return 1
    return 2


def getImgCoord(localCoord: tuple):
    if not isValid(localCoord):
        return (-1, -1)
    return (85 * localCoord[0] + 400, -50 * localCoord[1] + 720)


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


def MakeMoveOn(board, moves: list, localCoords: tuple, click=True):
    # Handle the board, for itself and its 6 neighbours
    for i in [localCoords, (localCoords[0], localCoords[1] + 2), (localCoords[0], localCoords[1] - 2), (localCoords[0] + 1, localCoords[1] + 1), (localCoords[0] + 1, localCoords[1] - 1), (localCoords[0] - 1, localCoords[1] + 1), (localCoords[0] - 1, localCoords[1] - 1)]:
        if isValid(i):
            board = setStateOnBoard(board, i)
    if click:
        moves.append(localCoords)
    return board


def solveBottom(board, moves: list, localCoords: tuple, click=True):
    south = (localCoords[0], localCoords[1] - 2)
    # Check if there is a bottom cell
    if isValid(south):
        if getStateFromBoard(board, localCoords) == 2:
            board = MakeMoveOn(board, moves, south, click)
    return board


def copyBoard(board):
    copy = []
    for i in range(len(board)):
        arr = []
        for j in range(len(board[0])):
            arr.append(board[i][j])
        copy.append(arr)
    return copy


def propogate(board, moves: list, click=True):
    # Doing things the hard way :D
    solveSequence = [(0, 6), (-1, 5), (-2, 4), (-3, 3), (1, 5), (2, 4), (3, 3),
                     (0, 4), (-1, 3), (-2, 2), (-3, 1), (1, 3), (2, 2), (3, 1),
                     (0, 2), (-1, 1), (-2, 0), (-3, -1), (1, 1), (2, 0), (3, -1),
                     (0, 0), (-1, -1), (-2, -2), (1, -1), (2, -2),
                     (0, -2), (-1, -3), (1, -3), (-0, -4)]

    for i in range(len(solveSequence)):
        board = solveBottom(board, moves, solveSequence[i], click)

    return board, moves


def solve(board, moves: list):
    copy = copyBoard(board)
    copy, moves = propogate(copy, moves, False)
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

    if solver[0]:
        board = MakeMoveOn(board, moves, (-3, 3))
    if solver[1]:
        board = MakeMoveOn(board, moves, (-2, 4))
    if solver[2]:
        board = MakeMoveOn(board, moves, (-1, 5))
    if solver[3]:
        board = MakeMoveOn(board, moves, (0, 6))

    board, moves = propogate(board, moves)
    return moves


def solveBoard(device):
    # 2. Get image
    take_screenshot(device, 'screen.png')
    image = Image.open('screen.png')
    Img = np.asarray(image)
    # 3. Get board state and store it into an array
    board = []
    for x in range(-3, 4):
        arr = []
        for y in range(-6, 7):
            arr.append(getState(Img, getImgCoord((x, y))))
        board.append(arr)
    # 4. Solve board and do bookkeeping
    moves = solve(board, [])
    t1 = time.time()
    for i in moves:
        sendClick(i)
    t2 = time.time()
    # 5. Reset and error check
    clickOn(400, 1120)
    if round(t2 - t1, 3) <= 1.800:
        take_screenshot(device, 'screen.png')
        print("Screenshotted")
    clickOn(69, 720)
    time.sleep(0.5)