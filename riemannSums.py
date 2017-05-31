import matplotlib
matplotlib.use('TkAgg')

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

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
a.grid(True)
xmax = 3.0
xmin = 0.0
xstep = .01
nstep = 30
t = arange(xmin, xmax, xstep)
function = "x^2"
variable = 'x'
integralstep = 1.0
root = Tk.Tk()
root.wm_title("Riemann Sums")
parser = Parser()

def mathFunction(x, function, variable):
    yVals = []
    print function
    for xVal in x:
        try:
            yVals.append(parser.parse(function).evaluate({variable: xVal}))
        except Exception as e:
            if "variable" in str(e):
                variable = str(e)[-1:]
                continue
    return yVals

def plotArea():
    area = 0;
    xbars = arange(integralstep/2, xmax, integralstep)
    ybars = mathFunction(xbars, function, variable)
    a.bar(xbars, ybars, width=integralstep, fill=False)
    for h in ybars:
        area += h*integralstep;
    a.set_title("Area: " + str(area))

a.plot(t, mathFunction(t, function, variable))
plotArea()

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

def _decreaseStepGraph():
    global integralstep;
    integralstep = integralstep/2;
    _updateGraph()

def _updateEquation():
    global function;
    global integralstep
    integralstep = 1.0;
    newEquation = equationEditor.get("1.0", "end-1c")
    print "updateGraph triggered with equation: " + newEquation
    function = newEquation
    _updateGraph()
    equationEditor.delete('1.0', "end")

def _updateGraph():
    try:
        a.clear()
        a.set_xlabel("x")
        a.set_ylabel("y")
        a.grid(True)
        a.plot(t, mathFunction(t, function, variable))
        equationEditor.delete('1.0', "end")
        root.update_idletasks()
        plotArea();
        canvas.show()
    except Exception as e:
        a.clear()
        a.set_xlabel("x")
        a.set_ylabel("y")
        equationEditor.delete('1.0', "end")

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
