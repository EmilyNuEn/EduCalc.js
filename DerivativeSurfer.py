import matplotlib
import numpy as np
import threading
import sys
import sympy
from numpy import arange, sin, pi
matplotlib.use('TkAgg')
#import scipy
#from scipy import misc as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from py_expression_eval import Parser
from matplotlib.figure import Figure

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Derivative Surfer")
parser = Parser()
ticker = 0

def mathFunction(x, function, variable):
    yVals = []
    for xVal in x:
        try:
            yVals.append(parser.parse(function).evaluate({variable: xVal}))
        except Exception as e:
            if "variable" in str(e):
                variable = str(e)[-1:]
                continue
    return yVals

f = Figure(figsize=(5, 4), dpi=100)
graph = f.add_subplot(111)
graph.grid(True)
t = arange(1.0, 4 * np.pi, 0.1)
function = "sin(x)"
variable = 'x'

graph.plot(t, mathFunction(t, function, variable))
# a.show()

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

stepSize = .25
TIME_DELAY = .5
xRange = np.arange(1.0, 14.0, stepSize)
tangentRange = np.arange(-1, 0, stepSize)

def init():
    global xRange

  # threading.Timer(1, createNewTangent).start()
  # threading.Timer(2, createNewTangent).start()

    for count in range(0, len(xRange)):
        threading.Timer(TIME_DELAY * count, createNewTangent).start()

def _quit():
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def updatePlot():
    global tangent
    graph.clear()
    graph.grid(True)
    graph.set_xlim([0, 14])
    graph.set_ylim([-4, 4])
    graph.plot(xRange, mathFunction(xRange, function, variable), 'b',
               tangentRange, mathFunction(tangentRange, tangent, variable), 'r')
    canvas.show()
    root.update_idletasks()

def restartAnimation():
    global xrange, ticker
    ticker = 0
    for count in range(0, len(xRange)):
        threading.Timer(TIME_DELAY*count, createNewTangent()).start()


def _updateEquation():
    global function, tangent
    newEquation = equationEditor.get("1.0", "end-1c")
    function = newEquation
    tangent = ""
    equationEditor.delete('1.0', "end")
    restartAnimation()
    updatePlot()

def get_derivative(function, xLoc):
    derivativeExpression = sympy.diff(function, variable, 1)
    return derivativeExpression.subs(variable, xLoc)


def updateTangent(newX, newY):
    global tangent
    tangent = str(get_derivative(function, newX)) + "*(x-" + str(newX) + ") + " + str(newY)


def createNewTangent():
    global tangentRange, ticker, parser, stepSize
    new_x = xRange[ticker]
    new_y = parser.parse(function).evaluate({variable: new_x})
    updateTangent(new_x, new_y)
    tangentRange = np.arange(new_x - 2, new_x + 2, stepSize)
    ticker += 1
    updatePlot()


def checkForEnterButton(event):
    if (event.keysym == 'Return'):
        _updateEquation()


graph.set_xlabel("x")
graph.set_ylabel("y")
graph.set_xlim([0, 14.0])
graph.set_ylim([-4, 4])
equationEditor = Tk.Text(master=root, height=1, width=30)
functionLabel = Tk.Label(master=root, text='f(x)=')
drawButton = Tk.Button(master=root, text='Graph', command=_updateEquation)
quitButton = Tk.Button(master=root, text='Quit', command=_quit)
functionLabel.pack(side=Tk.LEFT)
equationEditor.pack(side=Tk.LEFT)
drawButton.pack(side=Tk.RIGHT)
quitButton.pack(side=Tk.RIGHT)
root.bind("<KeyPress>", checkForEnterButton)

init()

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.