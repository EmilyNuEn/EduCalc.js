import matplotlib
matplotlib.use('TkAgg')
import matplotlib.lines as lines
from numpy import arange
import numpy as np
import sympy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from py_expression_eval import Parser
from matplotlib.figure import Figure
from textwrap import wrap

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Taylor Polynomials")


parser = Parser()


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
t = arange(0.0, 4 * np.pi, 0.01)
function = "sin(x)"
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

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def updatePlot():
    graph.clear()
    graph.grid(True)
    graph.set_ylim([-1.5, 1.5])
    graph.set_xlim([-0.5, 14.0])
    graph.plot(t, mathFunction(t, function, variable), 'b', t, mathFunction(t, taylorPolynomial, variable), 'r')
    blue_legend_line = lines.Line2D([], [], color='blue', label="f(x) = " + function)
    red_legend_line = lines.Line2D([], [], color='red', label="Taylor Polynomial of Degree " + str(polynomialDegree))
    polynomialLabel = graph.set_title("\n".join(wrap("P(x) = " + taylorPolynomial, 100)))
    graph.legend(handles=[blue_legend_line, red_legend_line])
    canvas.show()
    root.update_idletasks()

def _updateEquation():
    global function

    newEquation = equationEditor.get("1.0", "end-1c")
    function = newEquation
    equationEditor.delete('1.0', "end")
    resetPolynomial()
    updatePlot()

def getNthDerivative(function, xLoc, degree):
    derivativeExpression = sympy.diff(function, variable, degree)
    return derivativeExpression.subs('x', xLoc)

def func(x):
    mathFunction(x, function, variable)

def _addTermToPolynomial():
    global polynomialDegree, taylorPolynomial
    polynomialDegree += 1
    taylorPolynomial += " + (" + str(getNthDerivative(function, 0, polynomialDegree)) + "*x^" + str(polynomialDegree) + "/" + str(sympy.factorial(polynomialDegree)) + ")"
    updatePlot()

def resetPolynomial():
    global taylorPolynomial, polynomialDegree
    taylorPolynomial = getZerothPolynomial()
    polynomialDegree = 0

def checkForEnterButton(event):
	if(event.keysym == 'Return'):
		_updateEquation()

def getZerothPolynomial():
    return str(mathFunction([0], function, variable)[0])



polynomialDegree = 0
taylorPolynomial = getZerothPolynomial()
graph.set_xlabel("x")
graph.set_ylabel("y")
graph.set_ylim([-1.5, 1.5])
graph.set_xlim([-0.5, 14.0])
equationEditor = Tk.Text(master=root, height=1, width=30)
functionLabel = Tk.Label(master=root, text='f(x)=')
drawButton = Tk.Button(master=root, text='Graph', command=_updateEquation)
stepButton = Tk.Button(master=root, text='Step', command=_addTermToPolynomial)
quitButton = Tk.Button(master=root, text='Quit', command=_quit)
blue_legend_line = lines.Line2D([],[], color='blue', label="f(x) = " + function)
red_legend_line = lines.Line2D([], [], color='red', label="P(x) = " + taylorPolynomial)
graph.legend(handles=[blue_legend_line, red_legend_line])
functionLabel.pack(side=Tk.LEFT)
equationEditor.pack(side=Tk.LEFT)
drawButton.pack(side=Tk.RIGHT)
stepButton.pack(side=Tk.RIGHT)
quitButton.pack(side=Tk.RIGHT)
root.bind("<KeyPress>", checkForEnterButton)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.