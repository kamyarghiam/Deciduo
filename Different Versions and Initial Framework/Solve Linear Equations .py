from sympy import *
from sympy import sympify
from sympy.solvers.solveset import linsolve
from scipy.optimize import brenth

x0, x1, x2, x3, x4, L, Q, x, y=\
symbols('x0 x1 x2 x3 x4 L Q x y', real=True)

z = 0.012805
r = 0.012048
def almostEqual(x, y, epsilon = 10**-8):
    return abs(x-y) < epsilon

def a(x):
    return (5)*(((x*5)/(z)))**(1/(z-1))+(2)*(((x*2)/(r))**(1/(r-1))) - 20
b = brenth(a, 0.000001, 100000000)
print(b)


"""
#this minimizes 
from scipy.optimize import minimize
import numpy as np

def func(x, sign=-1.0):
    return sign*(x[0]**2 + x[1]**3)

#sign is negative to find maximum
def func_deriv(x, sign=-1.0):
    dfdx0 = sign*(2*x[0])
    dfdx1 = sign*(3*x[1]**2)
    return np.array([ dfdx0, dfdx1 ])
    
cons = ({'type': 'eq',
    'fun' : lambda x: np.array([5*x[0] + 2*x[1] -20])})
res = minimize(func, [-1.0,1.0], args=(-1.0,), jac=func_deriv, constraints=cons, method='SLSQP', options={'disp': False})

print(res.x)
"""