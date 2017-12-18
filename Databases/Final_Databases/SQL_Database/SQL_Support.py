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

#adds a new account to the database 
def addNewEntry(*args):
    #username,password,name,age,weight, parameter (1.5)
    parameters = list(args) + [1.5] + [1.5] +[5] +[5] + ["*"] + ["*"]
    
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    #these next two lines I got from stackoverflow 
    cursor = connection.execute('select * from accounts')
    names = list(map(lambda x: x[0], cursor.description))

    questionMarks = "(" + "?,"*(len(names)-1) + "?)"

    noRecords = ["No records from this day!"]*(len(names)-11)

    parameters += noRecords
    
    #this line of code was derived from:https://stackoverflow.com/questions/21142531/sqlite3-operationalerror-no-such-column
    cursor.execute("INSERT INTO accounts VALUES %s" % questionMarks, parameters)

    
    connection.commit()
    
    connection.close()

#allows you to see what's in the database
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

#adds a new date everytime you do something 
def addColumn(entry, date, username):
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    #these next two lines I got from stackoverflow 
    cursor = connection.execute('select * from accounts')
    names = list(map(lambda x: x[0], cursor.description))

    if date not in names:
        cursor.execute("ALTER TABLE accounts ADD COLUMN '%s' DEFAULT 'No records from this day!'"%(date))

    #gets the entry in the date column
    cursor.execute('SELECT "%s" FROM accounts WHERE username="%s"' %(date,username))
    dateRow = cursor.fetchall()

    if dateRow[0][0] == 'No records from this day!':
        cursor.execute("UPDATE accounts SET '%s'='%s' WHERE username='%s'"%(date,entry,username))
    else: 
        newEntry = dateRow[0][0] + " AND " + entry
        cursor.execute("UPDATE accounts SET '%s'='%s' WHERE username='%s'"%(date,newEntry,username))


    connection.commit()
    
    connection.close()

#sees which dates are enetered and which dates are not 
def retrieveDateInformation(date,username):
    connection = sqlite3.connect('Databases/Final_Databases/SQL_Database/Accounts.db')
    
    cursor = connection.cursor()
    
    #these next two lines I got from stackoverflow 
    cursor = connection.execute('select * from accounts')
    names = list(map(lambda x: x[0], cursor.description))

    if date not in names:
        connection.commit()
        connection.close()
        return "%s: No records from this day!" % date
    else: 
        #gets the entry in the date column
        cursor.execute('SELECT "%s" FROM accounts WHERE username="%s"' %(date,username))
        words = cursor.fetchall()[0][0]
        connection.commit()
        connection.close()
        return date + ": " + words

    
