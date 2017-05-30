import numpy as np
import matplotlib.pyplot as plt
from py_expression_eval import Parser

def f(t):
	yVals = []
	for xVal in t:
		yVals.append(parser.parse(function).evaluate({'x': xVal}))
	return yVals

parser = Parser()
function = "x^2"
t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure(1)
plt.plot(t2, f(t2), 'k')

plt.show()