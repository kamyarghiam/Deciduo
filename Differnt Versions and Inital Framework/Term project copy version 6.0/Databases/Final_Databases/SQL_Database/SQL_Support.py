import sqlite3
#https://code.tutsplus.com/tutorials/database-handling-in-python--cms-25645

#http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

"""
connection = sqlite3.connect('Accounts.db')

cursor = connection.cursor()

#only need this once to create database
cursor.execute('create table accounts(username, password, name, age, weight, FoodParameter, ExerciseParameter, LastFoodStars, LastExerciseStars, LastFoodOperation, LastExerciseOperation)')

#this creates an entry everytime 
cursor.execute("insert into accounts values ('k', 'k','Kamyar Ghiam', 18,170, 1.5, 1.5, 5, 5, '*', '*')")

#this edits a specific value 
#cursor.execute("UPDATE accounts SET parameter=99 WHERE username='kamyarghiam'")

cursor.execute('SELECT rowid, * FROM "accounts"')
all_rows = cursor.fetchall()
print(all_rows) 

connection.commit()

connection.close()
"""


def addNewEntry(*args):
    #username,password,name,age,weight, parameter (1.5)
    parameters = tuple(list(args) + [1.5] + [1.5] +[5] +[5] + ["*"] + ["*"])
    
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    
    #this line of code was derived from:https://stackoverflow.com/questions/21142531/sqlite3-operationalerror-no-such-column
    cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)", parameters)

    
    connection.commit()
    
    connection.close()

def accessData():
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    
    cursor.execute('SELECT rowid, * FROM "accounts"')
    all_rows = cursor.fetchall()
    
    connection.commit()
    
    connection.close()
    
    return all_rows
    
def editParameter(foodOrExcerise,account, newParameter):
    #foodOrExcerise: FoodParameter or ExerciseParameter
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    
    cursor.execute("UPDATE accounts SET %s=%0.2f WHERE username='%s'"%(foodOrExcerise,newParameter,account))
    connection.commit()
    
    connection.close()

#allows you to put in a string
def editStringParameter(place, account,newParameter):
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    
    cursor.execute("UPDATE accounts SET %s='%s' WHERE username='%s'"%(place,newParameter,account))
    
    connection.commit()
    
    connection.close()


