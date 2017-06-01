import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
import numpy as np
import scipy
import sympy
from scipy import misc as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from py_expression_eval import Parser
from matplotlib.figure import Figure
import threading
import sys
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
t = arange(1.0, 4 * np.pi, 0.01)
function = "x^2"
variable = 'x'

graph.plot(t, mathFunction(t, function, variable))
#a.show()

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

TIME_DELAY = .01
xRange = np.arange(1.0, 14.0, .01)
tangentRange = np.arange(-1, 0, .01)

def init():
    global xRange
    for count in range(0, len(xRange)):
        threading.Timer(TIME_DELAY*count, createNewTangent).start()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def updatePlot():
    global tangent
    graph.clear()
    graph.grid(True)
    graph.plot(xRange, mathFunction(xRange, function, variable), 'b', tangentRange, mathFunction(tangentRange, tangent, variable), 'r')
    canvas.show()
    root.update_idletasks()

def _updateEquation():
    global function
    newEquation = equationEditor.get("1.0", "end-1c")
    function = newEquation
    equationEditor.delete('1.0', "end")
    updatePlot()

def getDerivative(function, xLoc):
    derivativeExpression = sympy.diff(function, variable, 1)
    return derivativeExpression.subs(variable, xLoc)

def updateTangent(newX, newY):
    global tangent
    print getDerivative(function, newX)
    tangent = str(getDerivative(function, newX)) + "*(x-" + str(newX) + ") + " + str(newY)
    print tangent

def createNewTangent():
    print "in createNewTangent"
    global tangentRange, ticker
    newX = xRange[ticker]
    print newX
    print function
    newY = parser.parse(function).evaluate({variable: newX})
    updateTangent(newX, newY)
    tangentRange = np.arange(newX - 1, newX + 1, .01)
    ticker += 1
    updatePlot()



def checkForEnterButton(event):
	if(event.keysym == 'Return'):
		_updateEquation()

graph.set_xlabel("x")
graph.set_ylabel("y")
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