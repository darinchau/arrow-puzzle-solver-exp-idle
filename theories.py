from solver import clickReverse, take_screenshot, cropReverse
from PIL import Image
import numpy as np
import time
import navigator
try:
    import pytesseract
except:
    pass


def init():
    global LastPublishMark
    if pytesseract == None:
        global ActiveStrategy
        ActiveStrategy = NoTheoriesForYou
        return
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# Constants
timer = 100
LastPublishMark = 0


def getrho(x1, y1, x2, y2):
    global timer
    try:
        # Gives it like 5 tries or so
        for _ in range(10):
            # Get last publish mark
            screen = take_screenshot('screen.png')
            im = Image.fromarray(cropReverse(x1, y1, x2, y2, screen))
            rho = pytesseract.image_to_string(im)
            if rho.find("e") > 0:
                break
            else:
                time.sleep(1)

        rho = rho.strip()
        rho = rho[rho.find("e") + 1:-1]
        print(rho)
        if len(rho) <= 0:
            print("Error: could not read rho")
            raise RuntimeError("Pytesseract error")
        rho = int(rho)
        return rho, screen
    except:
        # Some error occured during setup. Trying again later
        timer = 100
        print("Pytesseract error. Aborting theories")
        return 0, screen


def T5():
    global timer
    global LastPublishMark

    # Step 1: try to read current rho value
    rho, screen = getrho(491, 300, 523, 100)
    assert(type(screen) == np.ndarray)

    # Step 2: Determine checkbox status
    checkbox1 = cropReverse(643, 770, 643, 770, screen)[0] > 30
    checkbox2 = cropReverse(733, 770, 733, 770, screen)[0] > 30
    checkbox3 = cropReverse(823, 770, 823, 770, screen)[0] > 30
    checkbox4 = cropReverse(913, 770, 913, 770, screen)[0] > 30
    checkbox5 = cropReverse(979, 784, 979, 784, screen)[0] > 30
    c = (checkbox1, checkbox2, checkbox3, checkbox4, checkbox5)

    if rho < LastPublishMark - 10:
        print("Low stratting")
        # Set Checkboxes and buy c2
        if not c[0]:
            clickReverse(643, 770)
        if not c[1]:
            clickReverse(733, 770)
        if not c[2]:
            clickReverse(823, 770)
        if c[3]:
            clickReverse(913, 770)
        if not c[4]:
            clickReverse(979, 784)

        # Buy c2
        while not navigator.IsOnTheoryx1():
            clickReverse(561, 65)
        clickReverse(561, 65, repeat=4, wait=True)
        clickReverse(910, 400, wait=True)
        clickReverse(561, 65, wait=True)
        timer = 120

    elif rho < LastPublishMark + 5:
        print("High stratting")
        # Set Checkboxes and buy c1
        if not c[0]:
            clickReverse(643, 770)
        if not c[1]:
            clickReverse(733, 770)
        if c[2]:
            clickReverse(823, 770)
        if not c[3]:
            clickReverse(913, 770)
        if not c[4]:
            clickReverse(979, 784)

        # buying c1
        clickReverse(561, 65, repeat=4, wait=True)
        clickReverse(810, 400, wait=True)
        clickReverse(561, 65, wait=True)
        timer = 700

    else:
        print("Publishing")
        LastPublishMark = rho
        if not c[0]:
            clickReverse(643, 770)
        if not c[1]:
            clickReverse(733, 770)
        if not c[2]:
            clickReverse(823, 770)
        if c[3]:
            clickReverse(913, 770)
        if not c[4]:
            clickReverse(979, 784)

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
    rho, screen = getrho(491, 300, 523, 100)
    ActiveStrategy()
