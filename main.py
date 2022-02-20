from solver import *
from subprocess import call
import threading as thread
from tkinter import messagebox

_callbacks = {}
cap = 650

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
    print("Initializing")
    Event.on('solve', solveThis)
    Event.on('solve', emittingDone)
    initialize()

def emittingDone():
    pass

# Solves sthe board
def solveThis():
    solveBoard()

#######################################################################################################

stop_threads = False

# The accelerator part

# Handles the press accelerator event
def PressAccelerator():
    Event.off('solve', PressAccelerator)
    Event.on('solve', solveThis)
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

# Queues the accelerator event
def EnqueueAccelerator():
    i = 10
    global stop_threads
    while True:
        if i < 0:
            Event.off('solve', solveThis)
            Event.on('solve', PressAccelerator)
            print("Pressing accelerator")
            i = cap
        else:
            time.sleep(1)
            i -= 1
        if stop_threads:
            break

def CallBoardSolver():
    global stop_threads
    while True:
        try:
            Event.emit('solve')
        except IndexError:
            stop_threads = True
            messagebox.showerror("Dead Emulator", "Hey the emulator is dead")
        if stop_threads:
            break


#Main function
if __name__ == '__main__':
    init()
    
    t1 = thread.Thread(target = EnqueueAccelerator)
    t1.start()

    t2 = thread.Thread(target = CallBoardSolver)
    t2.start()

    stop = input()
    if stop == "stop" or stop_threads:
        Event.off('solve', solveThis)
        Event.off('solve', emittingDone)
        Event.off('solve', PressAccelerator)
        stop_threads = True