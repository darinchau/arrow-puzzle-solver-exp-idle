from solver import take_screenshot, cropReverse, clickReverse
import numpy as np
import check 
import time


def compare(arr1: np.ndarray, arr2: np.ndarray, threshold = 5, match = 0.9):
    if not arr1.shape == arr2.shape:
        return False
    arr1 = arr1.reshape(-1)
    arr2 = arr2.reshape(-1)
    s = np.count_nonzero(np.abs(arr1 - arr2) < threshold)
    return s/len(arr1) >= match


def print2Darray(im: np.ndarray):
    for i in range(im.shape[0]):
        print("[", end="")
        for j in range(im.shape[1] - 1):
            print(im[i][j], end=", ")
        print(im[i][-1], end="")
        print("]" if i == im.shape[0] - 1 else "],")


def Checker(coordinates: tuple, checker: np.ndarray, Image=None):
    if type(Image) == type(None):
        Image = take_screenshot('screen.png')
    im = cropReverse(coordinates[0], coordinates[1],
                     coordinates[2], coordinates[3], Image)
    im = im[:, :, 0]
    return compare(im, checker)


def IsOnTheories(Image=None):
    coordinates = (144, 775, 156, 754)
    checker = np.array(check.theory)
    return Checker(coordinates, checker, Image)


def IsOnArrowPuzzle(Image=None):
    coordinates = (64, 474, 76, 444)
    checker = np.array(check.arrow)
    return Checker(coordinates, checker, Image)


def IsOnStudents(Image=None):
    checker = np.array(check.students)
    coordinates = (144, 454, 166, 429)
    return Checker(coordinates, checker, Image)


def GiftAvailable(Image=None):
    checker = np.array(check.gift)
    coordinates = (1106, 428, 1126, 400)
    return Checker(coordinates, checker, Image)


def IsOnMain(Image=None):
    return GiftAvailable(Image) and not IsOnStudents(Image) and not IsOnTheories(Image)


def CheckLocation():
    Image = take_screenshot('screen.png')
    if IsOnTheories(Image):
        return "theories"
    if IsOnArrowPuzzle(Image):
        return "arrow"
    if IsOnStudents(Image):
        return "students"
    if IsOnMain(Image):
        return "main"
    return "not sure"


# Attempts to navigate to a given location. Returns true if we successfully arrived
def goto(destination):
    # Checking
    if destination not in ["theories", "students", "main", "arrow"]:
        print("Wrong destination variables: " + destination)
        raise AssertionError("Wrong destination variables: " + destination)

    location = CheckLocation()
    orig = location
    if location == destination:
        return True

    # Spams cross button for good measures
    print("Going from " + orig + " to " + destination)
    clickReverse(34, 34, repeat=5, wait = True)
    location = CheckLocation()

    # One of the main screen now
    if destination in ["theories", "students", "main"]:
        i = 0
        while location != destination and i < 5:
            clickReverse(1137, 86, wait = True)
            location = CheckLocation()
            i += 1
        if i > 5:
            return False
    
    elif destination == "arrow":
        if not GiftAvailable():
            clickReverse(34, 34, repeat=5, wait = True)
            time.sleep(5)
            return goto("arrow")
        
        # Minigame button, arrow puzzle, hard
        clickReverse(1137, 405, wait = True)
        clickReverse(840, 372, wait = True)
        clickReverse(689, 409, wait = True)

    # Checking
    if CheckLocation() != destination:
        return goto(destination)

    return True

def IsCheckBoxOn(Image=None):
    if not IsOnTheories(Image):
        return False
    checker = np.array(check.checkbox)
    coordinates = (1005, 794, 1035, 765)
    return Checker(coordinates, checker, Image)


def IsOnTheoryx1(Image=None):
    if not IsOnTheories(Image):
        return False
    checker = np.array(check.theoryx1)
    coordinates = (556, 131, 568, 90)
    return Checker(coordinates, checker, Image)

if __name__ == "__main__":
    coordinates = (1005, 794, 1035, 765)
    Image = take_screenshot('screen.png')
    im = cropReverse(coordinates[0], coordinates[1],
                     coordinates[2], coordinates[3], Image)
    im = im[:, :, 0]
    print2Darray(im)