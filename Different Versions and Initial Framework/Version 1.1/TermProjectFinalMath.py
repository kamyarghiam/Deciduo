from scipy.optimize import brenth
from Database import dictionary_of_food
from Exercise_Database_Final import dictionary_of_exercise
import decimal
#taken from course website
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
####################################
# Food 
####################################

class Food(object): 
    #module
    def __init__(self, discrete = None, healthy = [], happy = [],\
    calories = [], money = [], Wcalories = [], Wmoney = [], howhealthy = [],\
    howhappy = [], alpha = [], anotherinput =  True, countvariables = 0,\
    max = 2, min  = 1):
        self.max = max #maximum food items you can ask for 
        self.min = min
        self.discrete = discrete #checks if the food is divisible
        #Fixed Judgement
        self.healthy = healthy
        self.happy = happy
        #Costs
        self.calories = calories
        self.money = money
        #Constraints (W = willing to eat or pay)
        self.Wcalories = Wcalories
        self.Wmoney = Wmoney
        #Variables judgement
        self.howhealthy = howhealthy
        self.howhappy = howhappy
        #Algorithm 
        self.alpha = alpha
        #Checks if user wants to input another food
        self.anotherinput = anotherinput 
        #Counts how many food items were added
        self.countvariables = countvariables 
    #solves for lambda and then can be used to get x and y values
    def lambdaSolverMoneyConstraint(self):
        epsilon = 10**-8
        delta = 10**8
        #calculated function of legranage optimization (derviation can be shown)
        def function(x):
            a1 = self.alpha[0] #alpha values
            a2 = self.alpha[1]
            m1 = self.money[0] #money constraint
            m2 = self.money[1]
            return (m1)*(((x*m1)/(a1)))**(1/(a1-1))+(m2)*(((x*m2)/(a2))**(1/(a2-1))) - self.Wmoney[0]
        return brenth(function, epsilon, delta)
    def getValuesFromLambdaMoney(self):
        L = self.lambdaSolverMoneyConstraint() #lambda
        #these are calculated values 
        a1 =  self.alpha[0]
        a2 = self.alpha[1]
        m1 = self.money[0] #money constraint
        m2 = self.money[1]
        first_food = ((L*m1)/(a1))**(1/(a1-1))
        second_food = ((L*m2)/(a2))**(1/(a2-1))
        return [first_food, second_food]
    def lambdaSolverCalorieConstraint(self):
        epsilon = 10**-8
        delta = 10**8
    #calculated function of legranage optimization (derviation can be shown)
        def function(x):
            a1 = self.alpha[0] #alpha values
            a2 = self.alpha[1]
            c1 = self.calories[0] #calorie constraint
            c2 = self.calories[1]
            return (c1)*(((x*c1)/(a1)))**(1/(a1-1))+(c2)*(((x*c2)/(a2))**(1/(a2-1))) - self.Wcalories[0]
        return brenth(function, epsilon, delta)

    def getValuesFromLambdaCalorie(self):
        L = self.lambdaSolverCalorieConstraint() #lambda
        #these are calculated values 
        a1 =  self.alpha[0]
        a2 = self.alpha[1]
        c1 = self.calories[0] #calorie constraint
        c2 = self.calories[1]
        first_food = ((L*c1)/(a1))**(1/(a1-1))
        second_food = ((L*c2)/(a2))**(1/(a2-1))
        return [first_food, second_food]
    def collectInitialself(self):
        #Constraints (W = willing to eat or pay)
        (self.Wcalories).append(int(input("How many calories are you willing to eat? ")))
        (self.Wmoney).append(int(input("How much money are you willing to spend in total? ")))
        #Variables judgement
        (self.howhealthy).append(\
        int(input("How important is it for you to be healthy in this meal?(From 1-10) ")))
        (self.howhappy).append(int(input("How important is it for you to feel satisfied from this meal?(from 1-10) ")))
        discrete = input("Is your food divisble? (i.e. do you want some of each food?) ")
        if discrete == "Yes":
            self.discrete = False
        else: self.discrete = True
        
    def checkDictioanryOfFood(self, search):
        search = search.lower()
        results = []
        for food in dictionary_of_food:
            if search in food.lower():
                results.append([food, dictionary_of_food[food]])
        if results == []:
            return False
        return results

    def collectFood(self):
        self.countvariables += 1
        #Fixed Judgement
        print()
        print("Food item %d:" % self.countvariables)
        print()
        food = input("What is the name of your food? ")
        results = self.checkDictioanryOfFood(food)
        if results == False:
            print("Sorry, we don't have that food. Please enter it manually.")
            self.newFoodItem()
        else: 
            print("Which do you want?" )
            print()
            print(results)
        #####PRINT POSSIBLE FOOD ITEMS AND ASK WHICH THEY WANT 
        ###THEN, APPEND THEIR ANSWER TO THE DATA 
        ###LATER, YOU NEED TO BE ABLE TO EDIT DICTIONARY
            print()
            result = results[0] #CHANGE THIS
            print("Okay, you selected %s" % result[0])#CHANGE THIS
            (self.healthy).append(result[1][3])
            (self.calories).append(result[1][0])
        print()
        #variable judgemnet
        (self.happy).append(int(input(\
        "How happy would it make you to eat one serving?(From 1-10) ")))
        (self.money).append(int(input("How much does it cost per serving (In dollars)? ")))
        if 1 < self.countvariables < self.max-1:
            anotherinput = input("Do you want to add another food item?(Yes or No) ")
            if anotherinput == "No":
                self.anotherinput = False
            
    def newFoodItem(self):
        (self.healthy).append(int(input("How healthy is this food item?(From 1-10) ")))
        #Costs
        (self.calories).append(int(input("How many calories is one serving? ")))
        
    def getAlpha(self):
        h1 = self.howhealthy[0]
        h2 = self.howhappy[0]
        t1x = self.healthy[0]
        t1y = self.healthy[1]
        t2x = self.happy[0]
        t2y = self.happy[1]
        alpha1 = 1/(h1*t1y + h2*t2y) #This is a calculated values based on a formula I created
        alpha2 = 1/(h1*t1x + h2*t2x)
        (self.alpha).append(alpha1)
        (self.alpha).append(alpha2)
    def compareUtilityFunction(self):
        #finds the smaller utility inside constraints
        def utilityFunction(x, y):
            return x**(self.alpha[0]) + y**(self.alpha[1])
        x1 = self.money_solution[0]
        y1 = self.money_solution[1]
        x2 = self.calorie_solution[0]
        y2 = self.calorie_solution[1]
        if utilityFunction(x1, y1) <= utilityFunction(x2, y2):
            answer = [x1,y1]
        else: answer = [x2,y2]
        #finds the better food 
        if answer[0] >= answer[1]:
            better_food = "1"
        else: better_food = "2"
        print(answer)
        if self.discrete == True:
            return "Food item %s is the better choice" % better_food 
        else: return "I would have %0.2f servings of food item 1 and %0.1f servings"\
        % (answer[0], answer[1]) + " of food item 2" 

################

def runFood():
    food = Food()
    food.collectInitialself() 
    food.collectFood() 
    while food.anotherinput and food.countvariables < food.max:
        food.collectFood()
    food.getAlpha()
    food.money_solution = food.getValuesFromLambdaMoney()
    food.calorie_solution = food.getValuesFromLambdaCalorie()
    print(food.compareUtilityFunction())

#############


    

    


####################################
# Exercise 
####################################

#could not use inherticance because the optimization algorithm is different
class Exercise(object):
    def __init__(self, max = 5, min = 1, discrete = None, happy = [],\
    calpermin = [], Wtime = [], Mcalories = [], howhappy = [], alpha = [],\
    anotherinput =  True, countvariables = 0, age = 0, weight = 0):
        #module
        self.max = max #maximum exercise items you can ask for 
        self.min =  min
        self.discrete = discrete #checks if you can do multiple exercises
        #Fixed Judgement
        self.happy = happy
        self.calpermin = calpermin
        #Constraints (W = willing time. M is minimum calories wanted to be burned)
        self.Wtime = Wtime
        self.Mcalories = Mcalories
        #Variables judgement
        self.howhappy = howhappy
        #Algorithm 
        self.alpha = alpha
        self.anotherinput =  anotherinput #Checks if user wants to input another exercise
        self.countvariables = countvariables #Counts how many exercise items were added
        self.age = age
        self.weight = weight

    def getAlpha(self):
        maximum = 11 #I chose 11 because I don't want to get a divide by 0 error when subtracting maximum (10)
        h = (maximum - self.howhappy[0])
        for i in range(len(self.happy)):
            h1 = maximum - self.happy[i]
            alpha = 1/(2*h*h1) #calculated values based on a formula I created
            (self.alpha).append(alpha)
        
    
    def collectInitialself(self):
        #Constraints (W = willing to eat or pay)
        (self.weight) = (int(input("How much do you weigh? ")))
        (self.age) = (int(input("How old are you? ")))
        (self.Mcalories).append(int(input("How many calories do you want to burn? ")))
        #Variables judgement
        (self.howhappy).append(\
        int(input("How important is it for you to enjoy this workout?(From 1-10) ")))
        discrete = input("Do you want to do multiple workouts? (i.e. split your time between workouts?) ")
        if discrete == "Yes":
            self.discrete = False
        else: self.discrete = True
        
    def collectExercise(self):
        minutes = 60
        self.countvariables += 1
        #Fixed Judgement
        print()
        print("Exercise item %d:" % self.countvariables)
        print()
        exercise = input("What is the name of your exercise? ")
        results = self.checkDictioanryOfExercise(exercise)
        if results == False:
            print("Sorry, we don't have that exercise. Please enter it manually.")
            self.newExerciseItem()
        else: 
            print("Which do you want?" )
            print()
            print(results)
        #####PRINT POSSIBLE FOOD ITEMS AND ASK WHICH THEY WANT 
        ###THEN, APPEND THEIR ANSWER TO THE DATA 
        ###LATER, YOU NEED TO BE ABLE TO EDIT DICTIONARY
            print()
            result = results[0] #CHANGE THIS
            print("Okay, you selected %s" % result[0])#CHANGE THIS 
            if self.weight<=130:
                (self.calpermin).append(result[1][0]/minutes)
            elif self.weight <= 155:
                (self.calpermin).append(result[1][1]/minutes)
            elif self.weight <= 180:
                (self.calpermin).append(result[1][2]/minutes)
            else: (self.calpermin).append(result[1][3]/minutes)
        #Costs
        (self.happy).append(int(input("How happy does this workout make you?(From 1-10) ")))
        #checks if we want to add another exercise
        if 1 < self.countvariables < self.max-1:
            anotherinput = input("Do you want to add another workout?(Yes or No) ")
            if anotherinput == "No":
                self.anotherinput = False
                minimum_time = roundHalfUp(self.Mcalories[0]/max(self.calpermin))
                print(minimum_time, self.Mcalories, self.calpermin)
                statement = "How much time are you willing to spend?(in minutes) Value must be larger than %0.1f minutes. " % minimum_time
                (self.Wtime).append(int(input(statement))) 
        else: 
        #makes sure there is more than one variable
            if self.countvariables > 1:
                self.anotherinput = False
                minimum_time = self.Mcalories[0]/max(self.calpermin)
                statement = "How much time are you willing to spend?(in minutes) Value must be larger than %0.1f minutes. " % minimum_time
                (self.Wtime).append(int(input(statement))) 
    def checkDictioanryOfExercise(self, search):
        search = search.lower()
        results = []
        for exercise in dictionary_of_exercise:
            if search in exercise.lower():
                results.append([exercise, dictionary_of_exercise[exercise]])
        if results == []:
            return False
        return results
    
    def newExerciseItem(self):
        minutes = 60
        calperminute = (int(input("How many calories per hour do you burn from this exercise? ")))/minutes
        (self.calpermin).append(calperminute)

    def newFoodItem(self):
        (self.healthy).append(int(input("How healthy is this food item?(From 1-10) ")))
        #Costs
        (self.calories).append(int(input("How many calories is one serving? ")))
    
    #solves for lambda and then can be used to get x and y values
    def lambdaConstraintSolver(self):
        #these variables are used to provide constraints on linear solver
        epsilon = 10**-15
        delta = 10**15
        #calculated function of legranage optimization (derviation can be shown)
        def function(x):
            def lambdaSolver(x,al):
                alpha = al
                try: return (x/alpha)**(1/(alpha-1))
                #if we get a divide by 0 error, lambda becomes 1 
                except: return 1
            equation = 0 
            for i in self.alpha:
                equation += lambdaSolver(x,i)
            return equation - self.Wtime[0]
        return brenth(function, epsilon, delta)
        
    def getValuesFromLambda(self):
        L = self.lambdaConstraintSolver() #lambda
        #these are calculated values 
        exerciseList = []
        for i in self.alpha:
            alpha = i
            exerciseList += [(L/alpha)**(1/(alpha-1))]
        better_exercise = max(exerciseList)
        better = exerciseList.index(better_exercise) + 1
        if self.discrete == True:
            return "Exercise %s is the best choice" % better
        else: 
            if len(exerciseList) == 2:
                return "You should do exercise 1 for %0.2f minutes and exercise 2 for %0.2f minutes"\
                % (exerciseList[0], exerciseList[1])
            elif len(exerciseList) == 3:
                return "You should do exercise 1 for %0.2f minutes, exercise 2 for %0.2f minutes, and exercise 3 for %0.2f minutes"\
                % (exerciseList[0], exerciseList[1], exerciseList[2]) 
            elif len(exerciseList) == 4:
                return "You should do exercise 1 for %0.2f minutes, exercise 2 for %0.2f minutes, exercise 3 for %0.2f minutes, and exercise 4 for %0.2f minutes"\
                % (exerciseList[0], exerciseList[1], exerciseList[2], exerciseList[3])
            elif len(exerciseList) == 5:
                return "You should do exercise 1 for %0.2f minutes, exercise 2 for %0.2f minutes, exercise 3 for %0.2f minutes, exercise 4 for %0.2f minutes, and exercise 5 for %0.2f minutes"\
                % (exerciseList[0], exerciseList[1], exerciseList[2], exerciseList[3], exerciseList[4]) 

##########
def runExercise():
    exercise = Exercise()
    exercise.collectInitialself() 
    exercise.collectExercise() 
    #collect the data until the user says no more
    while exercise.anotherinput and exercise.countvariables<exercise.max:
        exercise.collectExercise()
        exercise.getAlpha()
    print(exercise.getValuesFromLambda())
#########