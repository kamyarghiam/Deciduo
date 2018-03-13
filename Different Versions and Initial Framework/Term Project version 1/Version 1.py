#This import is a library that helps with the derivatives. 
from sympy import *
from sympy import sympify
from sympy import symbols, diff, sympify
"""This line is necessary for running the derivatives. Takes up to 5 variables
These variables will be reserved for the equations"""
#Use diff(f, x) t0 take partial derivative of f with respect to x
x0, x1, x2, x3, x4, L, Q=\
symbols('x0 x1 x2 x3 x4 L Q', real=True)

#This is for solving systems of equaionts 
from sympy.solvers.solveset import linsolve


def run():
    class Struct(object): pass
    data = Struct()
    data.max = 2 #maximum food items you can ask for 
    data.min = 1
    #Fixed Judgement
    data.healthy = [6,5]#CHANGE
    data.happy = [6,7]#CHANGE
    #Constraints/Costs (W = willing to eat or pay)
    data.calories = [100,200]#CHANGE
    data.money = [5,2]#CHANGE
    data.Wcalories = [800]#CHANGE
    data.Wmoney = [20]#CHANGE
    #Variables judgement
    data.howhealthy = [4]#CHANGE
    data.howhappy = [9]#CHANGE
    #Algorithm 
    data.alpha = []#CHANGE
    data.anotherinput =  True #Checks if user wants to input another food
    data.countvariables = 2  #CHANGE #Counts how many food items were added
    #collectInitialData(data) 
    #collectData(data)
    while data.anotherinput and data.countvariables<data.max:
         collectData(data)
    getAlpha(data)
    solution = solveLegrangeGradientFunctions(data)
    return solution 

def collectInitialData(data):
    #Constraints (W = willing to eat or pay)
    (data.Wcalories).append(int(input("How many calories are you willing to eat? ")))
    (data.Wmoney).append(int(input("How much money are you willing to spend in total? ")))
    #Variables judgement
    (data.howhealthy).append(\
    int(input("How important is it for you to be healthy in this meal?(From 1-10) ")))
    (data.howhappy).append(int(input("How important is it for you to feel satisfied from this meal?(from 1-10) ")))
def collectData(data):
    data.countvariables += 1
    #Fixed Judgement
    print()
    print("Food item %d:" % data.countvariables)
    print()
    (data.healthy).append(int(input("How healthy is this food item?(From 1-10) ")))
    (data.happy).append(int(input(\
    "How happy would it make you to eat one serving?(From 1-10) ")))
    #Costs
    (data.calories).append(int(input("How many calories is one serving? ")))
    (data.money).append(int(input("How much does it cost per serving (In dollars)? ")))
    if 1 < data.countvariables < data.max-1:
        anotherinput = input("Do you want to add another food item?(Yes or No) ")
        if anotherinput == "No":
            data.anotherinput = False

def getAlpha(data):
    h1 = data.howhealthy[0]
    h2 = data.howhappy[0]
    for i in range(data.countvariables):
        t1 = data.healthy[i]
        t2 = data.happy[i]
        alpha = 1/(h1*t1 + h2*t2) #This is a calculated values based on a formula I created
        (data.alpha).append(alpha)
    
def gradientFunctions(data):

    #returns list with gradient functions
    gradient_functions = []
    if data.countvariables == 2:
        function1 = diff(x0**data.alpha[0] - L*data.money[0]*x0, x0)
        function2 = diff(x1**data.alpha[1] - L*data.money[1]*x1, x1)
        gradient_functions.append(function1)
        gradient_functions.append(function2)
    return gradient_functions

def getConstraints(data): 
    constraints = []
    #For calories 
    final_cal_equation = "%d*(-1)" % data.Wcalories[0]
    cal_equation = ""
    for i in range(len(data.calories)):
        x = "x" + str(i) 
        cal = data.calories[i]
        cal_equation += str(cal) + "*"  + x + "+"
    final_cal_equation = cal_equation + final_cal_equation
    constraints += [final_cal_equation]
    """
    #For money 
    final_money_equation = "%d*(-1)" % data.Wmoney[0]
    money_equation = ""
    for i in range(len(data.money)):
        x = "x" + str(i) 
        money = data.money[i]
        money_equation += str(money) + "*"  + x + "+"
    final_money_equation = money_equation + final_money_equation
    constraints += [final_money_equation]
    """
    return constraints

def solveLegrangeGradientFunctions(data):
    gradient_functions = gradientFunctions(data)
    #Changes gradient functions into a list 
    #returns list with constraints, in the order of calories then money
    constraints = getConstraints(data) 
    new_constraints = []
    for i in constraints:
        #changes the type to something iterable for nonlinsolve
        new_constraints += [sympify(i)]
    #Solves for the legrange multipliers 
    #solves gradeitn for fist function
    solution1 = list(nonlinsolve([gradient_functions[0]], (L)))
    solution2 = list(nonlinsolve([gradient_functions[1]], (L)))
    solution_list = list(solution1[0]) + list(solution2[0])
    #subtracts second equation from first
    new_solutions = str(solution_list[0])+"-1*("+str((solution_list[1]))+")"
    #turns into correct type
    new_solution_list = [sympify(new_solutions)]

    legrange_functions = new_constraints + new_solution_list
    legrange_functions = list(legrange_functions)
    print(legrange_functions)
    return nonlinsolve(legrange_functions, (x1))

def startScreen(canvas,data):
    canvas.create_rectangle(0,0,data.width, data.height, fill = "gray")
    canvas.create_text(data.width/2, data.margin, font ="Helvitica 180",\
    text = "Deciduo")
    #buttons 
    foodButton = Button(200, 100, 2*data.width//3,data.height//2, "blue", "Food")
    exerciseButton = Button(200, 100, data.width//3,data.height//2, "blue", "Exercise")
    foodButton.drawBox(canvas)
    exerciseButton.drawBox(canvas)
    
   
class Button(object):
    def __init__(self, lengthx, lengthy, centerx, centery, color, text):
        self.startx = centerx-lengthx//2
        self.starty = centery-lengthy//2
        self.centerx = centerx
        self.centery= centery
        self.lengthx = lengthx
        self.lengthy = lengthy
        self.color = color 
        self.text = text
        self.width = 1 
    def drawRectangle(self,canvas):
        canvas.create_rectangle(self.startx,self.starty,self.startx+self.lengthx\
        ,self.starty+self.lengthy, fill = self.color, width = self.width)
    def drawShadow(self, canvas):
        canvas.create_line(self.startx, self.starty + self.lengthy,\
        self.startx+self.lengthx,self.starty+self.lengthy, width = self.width+2)
        canvas.create_line(self.startx+self.lengthx, self.starty,\
        self.startx+self.lengthx,self.starty+self.lengthy, width = self.width+2)
    def drawText(self, canvas):
        canvas.create_text(self.centerx,self.centery, text = self.text,\
        font = "Helvitica 30 bold")
    def drawBox(self,canvas):
        self.drawRectangle(canvas)
        self.drawShadow(canvas)
        self.drawText(canvas)
run()
