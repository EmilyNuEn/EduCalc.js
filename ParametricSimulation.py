import matplotlib
matplotlib.use('TkAgg')
import threading
from numpy import arange, sin, pi
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from py_expression_eval import Parser
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

TIMER_DELAY = .25
dt = .1
parser = Parser()
tick = 0

def incrementGraphs():
    global tick
    tick += 1
    tVals.append(dt*tick)
    xVals.append(parser.parse(xFunction).evaluate({variable: dt*tick}))
    yVals.append(parser.parse(yFunction).evaluate({variable: dt*tick}))


def updateGraphs():
    global canvas,t
    parametricGraph.plot(xVals, yVals, 'b')
    xGraph.plot(tVals, xVals, 'r')
    yGraph.plot(tVals, yVals, 'g')
    parametricGraph.grid(True)
    xGraph.grid(True)
    yGraph.grid(True)

    xGraph.set_ylim([-10, 10])
    xGraph.set_xlim([0, 3])

    yGraph.set_ylim([-10, 10])
    yGraph.set_xlim([0, 3])

    parametricGraph.set_ylim([-10, 10])
    parametricGraph.set_xlim([0, 10])

    canvas.show()
    root.update_idletasks()


def init(t):
    for time in range(0, len(t)):
        threading.Timer(TIMER_DELAY*time, incrementGraphs).start()
        threading.Timer((TIMER_DELAY*time + .1), updateGraphs).start()

def _restartAnimation():
    global tick, xVals, yVals, tVals, xFunction, yFunction
    t = np.arange(0, 3.0, dt)
    xFunction = xFunctionEditor.get("1.0", "end-1c")
    yFunction = yFunctionEditor.get("1.0", "end-1c")
    xFunctionEditor.delete("1.0", "end")
    yFunctionEditor.delete("1.0", "end")
    tick = 0
    xVals = []
    yVals = []
    tVals = []
    yGraph.set_title("y(t)= " + yFunction)
    xGraph.set_title("x(t)= " + xFunction)
    yGraph.clear()
    xGraph.clear()
    parametricGraph.clear()
    init(t)

root = Tk.Tk()
root.wm_title("Parametric Equations")

mainContainer = Figure(figsize=(5, 4), dpi=100)

parametricGraph = mainContainer.add_subplot(131)
xGraph = mainContainer.add_subplot(132)
yGraph = mainContainer.add_subplot(133)

parametricGraph.grid(True)
xGraph.grid(True)
yGraph.grid(True)

t = arange(0.0, 3.0, dt)
xFunction = "t^2"
yFunction = "-4.9*t^2"
variable = 't'

parametricGraph.set_title("Parametric")
xGraph.set_title("x = " + xFunction)
yGraph.set_title("y = " + yFunction)

xGraph.set_ylim([0, 10])
xGraph.set_xlim([0, 3])

yGraph.set_ylim([-50, 0])
yGraph.set_xlim([0, 3])

parametricGraph.set_ylim([-50, 0])
parametricGraph.set_xlim([0, 10])

tVals = []
xVals = []
yVals = []

init(t)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(mainContainer, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
xFunctionLabel = Tk.Label(master=root, text="x(t)= ")
xFunctionEditor = Tk.Text(master=root, height=1, width=30)

yFunctionLabel = Tk.Label(master=root, text="y(t)= ")
yFunctionEditor = Tk.Text(master=root, height=1, width=30)

graphButton = Tk.Button(master=root, text="graph", command=_restartAnimation)

xFunctionLabel.pack(side=Tk.LEFT)
xFunctionEditor.pack(side=Tk.LEFT)

yFunctionLabel.pack(side=Tk.LEFT)
yFunctionEditor.pack(side=Tk.LEFT)

graphButton.pack(side=Tk.RIGHT)
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.