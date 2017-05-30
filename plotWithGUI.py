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

root = Tk.Tk()
root.wm_title("Embedding in TK")


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

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
a.grid(True)
t = arange(0.0, 3.0, 0.01)
function = "x^2"
variable = 'x'

a.plot(t, mathFunction(t, function, variable))
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

def _updateGraph():
	newEquation = equationEditor.get("1.0", "end-1c")
	print "updateGraph triggered with equation: " + newEquation
	try:
		if(not(newEquation == "")):
			function = newEquation
			print function
			print t
			print variable
			a.clear()
			a.set_xlabel("x")
			a.set_ylabel("y")
			a.grid(True)	
			a.plot(t, mathFunction(t, function, variable))
			equationEditor.delete('1.0', "end")
			root.update_idletasks()
			canvas.show()
	except Exception as e:
		a.clear()
		a.set_xlabel("x")
		a.set_ylabel("y")
		equationEditor.delete('1.0', "end")


def checkForEnterButton(event):
	if(event.keysym == 'Return'):
		_updateGraph()


a.set_xlabel("x")
a.set_ylabel("y")
equationEditor = Tk.Text(master=root, height=1, width=30)
functionLabel = Tk.Label(master=root, text='f(x)=')
drawButton = Tk.Button(master=root, text='Graph', command=_updateGraph)
quitButton = Tk.Button(master=root, text='Quit', command=_quit)
functionLabel.pack(side=Tk.LEFT)
quitButton.pack(side=Tk.RIGHT)
equationEditor.pack(side=Tk.TOP)
drawButton.pack(side=Tk.RIGHT)
root.bind("<KeyPress>", checkForEnterButton)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.