from solver import *
import multiprocessing

device = initialize()
t = []

while True:
    t = solveBoard(device, t)