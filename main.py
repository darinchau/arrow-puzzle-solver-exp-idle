from email import message
import solver
from subprocess import call
import threading
from tkinter import messagebox
import time
import theories
import navigator
import msvcrt
import sys

_callbacks = {}


class Event():
    @staticmethod
    def on(event_name, f):
        if event_name in _callbacks and f in _callbacks[event_name]:
            return

        _callbacks[event_name] = _callbacks.get(event_name, []) + [f]

    # Emit is not really an event but just calling the functions in callback one by one
    @staticmethod
    def emit(event_name, *data):
        global stop_threads
        for f in _callbacks.get(event_name, []):
            f(*data)
            if stop_threads:
                break

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
    solver.initialize()
    theories.init()


def solve():
    navigator.goto("arrow")
    solver.solveBoard()

#######################################################################################################


stop_threads = False

# The accelerator part
# Handles the press accelerator event


def PressAccelerator():

    print("Pressing accelerator")
    Event.off('solve', PressAccelerator)
    navigator.goto("main")
    solver.clickOn(38, 326, True)

    # Accelerator
    call(["adb", "shell", "input", "swipe", str(67),
         str(181), str(67), str(181), str(3000)])
    solver.clickOn(38, 326, True)
    time.sleep(1)

# Queues the accelerator event


def CheckTheories():
    # pass
    print("Checking theories")
    Event.off('solve', CheckTheories)

    # Navigate to theories page
    navigator.goto("theories")
    theories.ActiveStrategy()

    # Failsave
    if theories.timer < 0:
        theories.timer = 100


__err_counter = 0
reseterrcap = 300
__reset_err = reseterrcap


def HandleError(err: Exception):
    global __err_counter, __reset_err
    __err_counter += 1
    __reset_err = reseterrcap

    print(err)
    time.sleep(10)
    call(["adb", "shell", "am", "start", "-a", "android.intent.action.MAIN",
         "-n", "com.conicgames.exponentialidle/crc64327945add1aba81c.MainActivity"])

    if __err_counter > 5:
        print("Exceeded max error count! Stopping")
        return False
    return True


def Decrement(counter: int, f, limit: int = 300):
    if counter < 0:
        Event.on("solve", f)
        return limit
    return counter - 1


def reset_err():
    global __err_counter
    __err_counter = 0


def EnqueueEvents():
    i1 = 13
    global stop_threads, __reset_err
    while not stop_threads:
        try:
            i1 = Decrement(i1, PressAccelerator,  650)
            theories.timer = Decrement(theories.timer, CheckTheories, 1000)
            __reset_err = Decrement(__reset_err, reset_err, reseterrcap)
            time.sleep(1)

        except Exception as err:
            if not HandleError(err):
                stop_threads = True
                messagebox.showerror("RIP emulator.")


def CallBoardSolver():
    global stop_threads
    while not stop_threads:
        try:
            Event.emit('solve')
        except Exception as err:
            if not HandleError(err):
                stop_threads = True
                messagebox.showerror("RIP emulator.")


def readInput(default, timeout = 5):
    class KeyboardThread(threading.Thread):
        def run(self):
            self.timedout = False
            self.input = ''
            while True:
                if msvcrt.kbhit():
                    chr = msvcrt.getche()
                    if ord(chr) == 13:
                        break
                    elif ord(chr) >= 32:
                        self.input += chr.decode('utf-8')
                if len(self.input) == 0 and self.timedout:
                    break    

    result = default
    it = KeyboardThread()
    it.start()
    it.join(timeout)
    it.timedout = True
    if len(it.input) > 0:
        # wait for rest of input
        it.join()
        result = it.input
    return result

def stop():
    global stop_threads
    stop_st = ""
    while stop_st == "" and not stop_threads:
        stop_st = readInput("", timeout = 2)
    stop_threads = True


# Main function
if __name__ == '__main__':
    init()

    t1 = threading.Thread(target=EnqueueEvents)
    t1.start()

    t2 = threading.Thread(target=CallBoardSolver)
    t2.start()

    while not stop_threads:
        time.sleep(1)
    
    Event.off('solve', solve)
    Event.off('solve', PressAccelerator)
    Event.off('solve', CheckTheories)
    solver.OnStop()
    stop_threads = True