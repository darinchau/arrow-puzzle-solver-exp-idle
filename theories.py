from solver import clickReverse, take_screenshot, cropReverse
from PIL import Image
import numpy as np
import time
import navigator, check

def init():
    pass


# Constants
timer = 12
__lastTimer = 12
LastPublishMark = 0

# Not really the publish multiplier but the ratio of y/x before it publishes
PublishMultiplier = 694200

def setTimer(t):
    global timer 
    timer = t
    global __lastTimer
    __lastTimer = t

def find_subsequence(arr, subarr, threshold = 5):
    s = len(arr) - len(subarr) + 1
    rolling = np.zeros((s,) + subarr.shape)
    for i in range(s):
        rolling[i] = arr[-len(subarr):]
        arr = arr[:-1]
    n = [navigator.compare(a, subarr, threshold) for a in rolling]
    return np.flip(n)

def cropAndFilter(x1, y1, x2, y2, screen):
    #Crop the image and calculate the p value
    r2 = cropReverse(x1, y1, x2, y2, screen)
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
    n = [str(i[0]) for i in positions]

    # Failsave
    if len(n) == 0:
        clickReverse(x1, y1, repeat = 5)
        clickReverse(x2, y2, repeat = 5)
        navigator.goto("theories")
        return cropAndFilter(x1, y1, x2, y2, take_screenshot("screen.png"))
    return int("".join(n))


def GetVariableValue(x1, y1, x2, y2, screen: np.ndarray, tolerance = 5):
    # Fail fail save
    if tolerance > 50:
        print("Failed getting e, trying again...")
        return 0
    
    # Turn image into array
    r = cropReverse(x1, y1, x2, y2, screen)
    cr = r[:, :, 0].transpose((1,0))

    # Find e
    e_pos = np.where(find_subsequence(cr, np.array(check.valuee)))[0]
    if e_pos.shape[0] == 0:
        return GetVariableValue(x1, y1, x2, y2, take_screenshot("screen.png"), tolerance + 5)
        
    first_viable_pixel = e_pos[0] + len(check.valuee)
    exponent = cropAndFilter(x1, y1-first_viable_pixel, x2, y2, screen)
    multiple = cropAndFilter(x1, y1, x2, y1 - first_viable_pixel - len(check.valuee), screen)
    return exponent + np.log10(multiple) - np.floor(np.log10(multiple))


# Sets the checkbox value to the intended value
def SetCheckBox(x, y, toggle, screen):
    while not navigator.IsCheckBoxOn(screen):
        clickReverse(1032,766, True)
        screen = take_screenshot("screen.png")
    state = cropReverse(x, y, x, y, screen)[0] > 30
    if state != toggle:
        clickReverse(x, y)

def BuyAllVariable(x, y, mode = 0, count = 1):
    while not navigator.IsOnTheoryx1():
        clickReverse(561, 65)
    clickReverse(561, 65, repeat = mode)
    clickReverse(x, y, repeat = count ,wait = True)
    if mode > 0:
        clickReverse(561, 65, repeat = 5 - mode, wait=True)

def BuyUntil(x1, y1, x2, y2, threshold):
    assert x2 - x1 == 32
    screen = take_screenshot('screen.png')
    var = GetVariableValue(x1, y1, x2, y2, screen)
    rho = GetVariableValue(491, 300, 523, 100, screen)
    if var == 0 or rho == 0:
        setTimer(min(60, __lastTimer))
        return False
    
    while var < rho + np.log10(threshold):            
        BuyAllVariable(x1, y1, count = 2)
        screen = take_screenshot('screen.png')
        rho = GetVariableValue(491, 300, 523, 100, screen)
        var = GetVariableValue(x1, y1, x2, y2, screen)
        # Fail save - cannot read variable, probably because it is greyed out
        if var == 0 or rho == 0:
            setTimer(min(60, __lastTimer))
            return False
    
    return True

def Publish():
    # Publish
    clickReverse(154, 38)
    clickReverse(710, 400, repeat=3, wait=True)
    clickReverse(785, 400, repeat=1, wait=True)
    clickReverse(880, 400, repeat=2, wait=True)
    clickReverse(400, 400, wait=True)
    clickReverse(730, 584, wait=True)
    clickReverse(75, 400, repeat=5, wait=True)

def T5():
    global LastPublishMark
    global __lastTimer

    # Step 1: try to read current rho value
    screen = take_screenshot('screen.png')
    rho = GetVariableValue(491, 300, 523, 100, screen)
    tau = GetVariableValue(491, 700, 523, 500, screen)
    
    print(f"Current rho = e{rho}. Current tau = e{tau}. Next publish at e{LastPublishMark + np.log10(PublishMultiplier)}")
    if tau == 0 or rho == 0:
        setTimer(min(60, __lastTimer))
        return

    # Step 2: Determine checkbox status
    def SetBoxes(settings):
        SetCheckBox(643, 770, settings[0], screen)
        SetCheckBox(733, 770, settings[1], screen)
        SetCheckBox(823, 770, settings[2], screen)
        SetCheckBox(913, 770, settings[3], screen)
        SetCheckBox(979, 784, settings[4], screen)

    if LastPublishMark == 0:
        if not navigator.IsPublishable(screen):
            LastPublishMark = tau
        else:
            SetBoxes([False, True, False, True, True])
            print("Theory 5: High stratting + Publish")
            BuyUntil(787, 135, 819, 1, 0.04)
            BuyUntil(611, 135, 643, 1, 0.04)
            SetBoxes([True, True, True, False, True])
            nextpub = np.log10(42042069) + rho
            print(f"Theory 5: Publishing. Next publish at: e{nextpub}")
            LastPublishMark = rho
            Publish()
            setTimer(1)
            BuyAllVariable(910, 400, 1, 10)
        T5()
        return

    if rho < LastPublishMark - 10:
        # Set Checkboxes and buy c2
        SetBoxes([True, True, True, False, True])
        print("Theory 5: Low stratting")
        while not BuyUntil(875, 135, 907, 1, 0.01):
            # Triggered failsave
            BuyAllVariable(900, 400, mode = 2, count = 5)
        setTimer(__lastTimer + 4) 

    # Publish at multiplier >= 7.62
    elif rho < LastPublishMark + np.log10(PublishMultiplier):
        # Set Checkboxes and buy c1
        SetBoxes([False, True, False, True, True])
        print("Theory 5: High stratting")
        BuyUntil(787, 135, 819, 1, 0.04)
        BuyUntil(611, 135, 643, 1, 0.04)
        setTimer(180)

    else:
        SetBoxes([True, True, True, False, True])
        nextpub = np.log10(PublishMultiplier) + rho
        print(f"Theory 5: Publishing. Next publish at: e{nextpub}")
        LastPublishMark = rho
        Publish()
        setTimer(1)

        # c2 starts at 75 so gotta let it buy some on its own otherwise check rho cannot detect the value
        BuyAllVariable(910, 400, 1, 10)
        T5()


def NoTheoriesForYou():
    pass

#####################################################################################################


ActiveStrategy = T5

if __name__ == "__main__":
    init()
    ActiveStrategy()