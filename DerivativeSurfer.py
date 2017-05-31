import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from py_expression_eval import Parser

from matplotlib.figure import Figure
import sched
import time

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk



def _evaluateFunction(xVal):
    return Parser.parse(function, {'x': xVal})

def _updateGraph():
    try:
        a.clear()
        a.set_xlabel("x")
        a.set_ylabel("y")
        a.grid(True)
        a.plot(t, mathFunction(t, function, variable))
        a.plot(t, linearFunction(t[ticker * dx: ticker * dx + 10], dx * ticker, _evaluateFunction(dx * ticker)))
        equationEditor.delete('1.0', "end")
        root.update_idletasks()
        canvas.show()
    except Exception as e:
        a.clear()
        a.set_xlabel("x")
        a.set_ylabel("y")
        equationEditor.delete('1.0', "end")


def _updateTangent():
    global ticker
    ticker += 1
    _updateGraph()

def mathFunction(x, function, variable):
    yVals = []
    derivative = []
    print function
    for xVal in range(0, len(x)):
        yVals.append(parser.parse(function).evaluate({variable: xVal}))
        sched.scheduler(timeDelay*xVal + .5, _updateTangent())
        derivative.append((parser.parse(function).evaluate({variable: xVal + dx}) - yVals[xVal]) / dx)
    return yVals, derivative

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
a.grid(True)
xmax = 3.0
xmin = 0.0
xstep = .01
nstep = 30
timeDelay = .01
dx = .001
t = arange(xmin, xmax, xstep)
function = "x^2"
variable = 'x'
integralstep = 1.0
root = Tk.Tk()
ticker = 0
root.wm_title("Derivative Surfer")
parser = Parser()

a.plot(t, mathFunction(t, function, variable))

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _updateEquation():
    global equationEditor
    global function
    newEquation = equationEditor.get("1.0", "end-1c")
    print "updateGraph triggered with equation: " + newEquation
    function = newEquation
    _updateGraph()
    equationEditor.delete('1.0', "end")




def linearFunction(xVals, x1, y1):
    global derivative
    yVals = []
    for x in range(0, len(xVals)):
        yVals.append(derivative[x + ticker] * (xVals[x] - x1) + y1)
    return



def checkForEnterButton(event):
    if(event.keysym == 'Return'):
        _updateEquation()

#n, bins, patches = a.hist(generateBars(mathFunction(t, function, 'x')), orientation='vertical')
a.set_xlabel("x")
a.set_ylabel("y")
equationEditor = Tk.Text(master=root, height=1, width=30)
functionLabel = Tk.Label(master=root, text='f(x)=')
drawButton = Tk.Button(master=root, text='Graph', command=_updateEquation)
stepButton = Tk.Button(master=root, text='Step', command=_decreaseStepGraph)
quitButton = Tk.Button(master=root, text='Quit', command=_quit)
functionLabel.pack(side=Tk.LEFT)
equationEditor.pack(side=Tk.LEFT)
drawButton.pack(side=Tk.RIGHT)
stepButton.pack(side=Tk.RIGHT)
quitButton.pack(side=Tk.RIGHT)
root.bind("<KeyPress>", checkForEnterButton)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
