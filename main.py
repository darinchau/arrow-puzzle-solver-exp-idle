from solver import *
from subprocess import call
import threading as thread

_callbacks = {}
cap = 3800

class Event():
    @staticmethod
    def on(event_name, f):
        _callbacks[event_name] = _callbacks.get(event_name, []) + [f]
        return f

    # Emit is not really an event but just calling the functions in callback one by one
    @staticmethod
    def emit(event_name, *data):
        [f(*data) for f in _callbacks.get(event_name, [])]

    @staticmethod
    def off(event_name, f):
        try: 
            _callbacks.get(event_name, []).remove(f)
        except ValueError:
            pass

################################################################################################################

def init():
    print("initializing")
    Event.on('done', solveThis)
    Event.on('done', emittingDone)
    return initialize()

def emittingDone(device):
    # print("Done!")
    pass

# Solves sthe board (recursively)
def solveThis(device):
    # print("Is solving")
    solveBoard(device)

#######################################################################################################

stop_threads = False

# The accelerator part

# Handles the press accelerator event
def PressAccelerator(device):
    Event.off('done', PressAccelerator)
    Event.on('done', solveThis)
    # Cross 1
    clickOn(764, 38, True)

    # Cross 2
    clickOn(764, 314, True)

    # Play
    clickOn(38, 326, True)

    x = 67
    y = 181
    # Accelerator
    call(["adb", "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(3000)])

    # pause
    clickOn(38, 326, True)

    # Minigame button
    clickOn(396, 1136, True)

    # Arrow puzzle
    clickOn(407, 853, True)

    # Hard
    clickOn(394, 690, True)

    time.sleep(1)

def ehehe():
    i = 10
    global stop_threads
    while True:
        if i < 0:
            Event.off('done', solveThis)
            Event.on('done', PressAccelerator)
            print("Pressing accelerator")
            i = cap
        else:
            time.sleep(1)
            i -= 1
            if i % 60 == 0:
                print(f"There is {int(i/60)} minutes until we press the button again")
        if stop_threads:
            break

def ahaha(device):
    global stop_threads
    while True:
        try:
            Event.emit('done', device)
        except IndexError:
            stop_threads = True
        if stop_threads:
            break

#Main function
if __name__ == '__main__':
    device = init()
    layout = [[sg.Text('Solving the arrow puzzle...')]]
    window = sg.Window('Arrow puzzle solver', layout)
    
    t1 = thread.Thread(target = ehehe)
    t1.start()

    newtuple = (device, )
    t2 = thread.Thread(target = ahaha, args = newtuple)
    t2.start()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            # Event.off('done', PressAccelerator)
            Event.off('done', solveThis)
            Event.off('done', emittingDone)
            stop_threads = True
            break