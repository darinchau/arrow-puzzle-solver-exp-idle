from solver import clickReverse, take_screenshot, cropReverse
from PIL import Image
import numpy as np
import time
import navigator, check

def init():
    pass


# Constants
timer = 12
LastPublishMark = 0

def find_subsequence(arr, subarr, threshold = 5):
    s = len(arr) - len(subarr) + 1
    rolling = np.zeros((s,) + subarr.shape)
    for i in range(s):
        rolling[i] = arr[-len(subarr):]
        arr = arr[:-1]
    n = [navigator.compare(a, subarr, threshold) for a in rolling]
    return np.flip(n)


def getrho(x1, y1, x2, y2, screen: np.ndarray):
    # Turn image into array
    r = cropReverse(x1, y1, x2, y2, screen)
    cr = r[:, :, 0].transpose((1,0))
    # Image.fromarray(r).show()
    # Find e
    e_pos = np.where(find_subsequence(cr, np.array(check.valuee)))[0]
    if e_pos.shape[0] == 0:
        e_pos = np.where(find_subsequence(cr, np.array(check.valuee), 15))[0]
        if e_pos.shape[0] == 0:
            print("Cannot find e!")
            return 0
    first_viable_pixel = e_pos[0] + len(check.valuee)
    # print(first_viable_pixel)

    #Crop the image and calculate the p value
    r2 = cropReverse(x1, y1 - first_viable_pixel, x2, y2, screen)
    cr2 = r2[:, :, 0].transpose((1,0))
    # Image.fromarray(r2).show()

    #Get the numbers and store them temporarily in an array
    positions = []
    for i in range(len(check.values)):
        num_pos = np.where(find_subsequence(cr2, np.array(check.values[i])))[0]
        if len(num_pos) > 0:
            positions += [[i, p] for p in num_pos]

    # Sort said array according to the positions they appeared in
    positions.sort(key = lambda e: e[1])
    # print(positions)
    n = [str(i[0]) for i in positions]
    rho = "".join(n)
    # print(rho)
    return int(rho)


# Sets the checkbox value to the intended value
def SetCheckBox(x, y, toggle, screen):
    state = cropReverse(x, y, x, y, screen)[0] > 30
    if state != toggle:
        clickReverse(x, y)

def BuyAllVariable(x, y):
    while not navigator.IsOnTheoryx1():
        clickReverse(561, 65)
    clickReverse(561, 65, repeat=4, wait=True)
    clickReverse(x, y, wait=True)
    clickReverse(561, 65, wait=True)


def T5():
    global timer
    global LastPublishMark

    # Step 1: try to read current rho value
    screen = take_screenshot('screen.png')
    rho = getrho(491, 300, 523, 100, screen)
    if type(screen) != np.ndarray or rho == 0:
        print("Encountered Unexpected Type Error! Returning...")
        timer = 60
        return

    if LastPublishMark == 0:
        LastPublishMark = rho
        return

    # Step 2: Determine checkbox status
    SetCheckBox(643, 770, True, screen)
    SetCheckBox(733, 770, True, screen)
    SetCheckBox(979, 784, True, screen)

    if rho < LastPublishMark - 10:
        print("Theory 5: Low stratting")
        # Set Checkboxes and buy c2
        SetCheckBox(823, 770, True, screen)
        SetCheckBox(913, 770, False, screen)
        BuyAllVariable(910, 400)
        timer = 120

    elif rho < LastPublishMark + 5:
        print("High stratting")
        # Set Checkboxes and buy c1
        SetCheckBox(823, 770, True, screen)
        SetCheckBox(913, 770, False, screen)
        BuyAllVariable(810, 400)
        timer = 700

    else:
        print("Publishing")
        LastPublishMark = rho
        SetCheckBox(823, 770, True, screen)
        SetCheckBox(913, 770, False, screen)

        # Publish
        clickReverse(154, 38)
        clickReverse(710, 400, repeat=3, wait=True)
        clickReverse(785, 400, repeat=1, wait=True)
        clickReverse(880, 400, repeat=2, wait=True)
        clickReverse(400, 400, wait=True)
        clickReverse(730, 584, wait=True)
        clickReverse(75, 400, repeat=5, wait=True)
        timer = 30


def NoTheoriesForYou():
    pass

#####################################################################################################


ActiveStrategy = T5

if __name__ == "__main__":
    init()
    # screen = take_screenshot('screen.png')
    # rho = getrho(491, 300, 523, 100 , screen)
    # print(rho)
    ActiveStrategy()