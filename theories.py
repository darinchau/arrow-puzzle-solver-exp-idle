import solver
import time

i = 10
while True:
    if i < 0:
        print("Publishing")
        solver.clickOn(38, 326, True)
        solver.clickOn(760, 154, True)
        solver.clickOn(400, 740, True)
        solver.clickOn(400, 470, True)
        solver.clickOn(200, 720, True)
        solver.clickOn(750, 229, True)
        solver.clickOn(38, 326, True)
        i = 2000
    else:
        i -= 1
        time.sleep(1)