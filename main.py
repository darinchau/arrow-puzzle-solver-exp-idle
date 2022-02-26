import solver
from subprocess import call
import threading as thread
from tkinter import messagebox
import time
import theories
import navigator

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
    Event.on('solve', solve)
    Event.on('solve', emittingDone)
    solver.initialize()
    theories.init()


def emittingDone():
    pass


def solve():
    navigator.goto("arrow")
    solver.solveBoard()

#######################################################################################################


stop_threads = False

# The accelerator part
# Handles the press accelerator event


def PressAccelerator():
    Event.off('solve', PressAccelerator)
    navigator.goto("main")
    solver.clickOn(38, 326, True)
    x = 67
    y = 181
    # Accelerator
    call(["adb", "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(3000)])
    solver.clickOn(38, 326, True)
    time.sleep(1)

# Queues the accelerator event

def CheckTheories():
    # pass

    Event.off('solve', CheckTheories)
    # Navigate to theories page
    navigator.goto("theories")
    theories.ActiveStrategy()


def EnqueueEvents():
    i1 = 10
    i2 = 12
    global stop_threads
    while True:
        try:
            if i1 < 0:
                Event.on('solve', PressAccelerator)
                print("Pressing accelerator")
                i1 = cap
            if i2 < 0:
                Event.on('solve', CheckTheories)
                print("Checking theories")
                i2 = theories.timer
            time.sleep(1)
            i1 -= 1
            i2 -= 1
        except:
            stop_threads = True
            messagebox.showerror("Dead Emulator", "Hey the emulator is dead")
        if stop_threads:
            break


def CallBoardSolver():
    global stop_threads
    while True:
        try:
            Event.emit('solve')
        except:
            stop_threads = True
            messagebox.showerror("Dead Emulator", "Hey the emulator is dead")
        if stop_threads:
            break


# Main function
if __name__ == '__main__':
    init()

    t1 = thread.Thread(target=EnqueueEvents)
    t1.start()

    t2 = thread.Thread(target=CallBoardSolver)
    t2.start()

    stop = input()
    if stop == "stop" or stop_threads:
        Event.off('solve', solve)
        Event.off('solve', emittingDone)
        Event.off('solve', PressAccelerator)
        Event.off('solve', CheckTheories)
        solver.OnStop()
        stop_threads = True
