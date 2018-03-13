import Databases.Final_Databases.FoodDatabase as FOOD

def addToFoodDictionary(food):
	#finds where to add it in the dictionary
	with open("Databases/Final_Databases/FoodDatabase.py") as file:  
		data = file.readlines() 
	dictionary = data[1]
	index = data[1].index("{")
	#creates entry
	entryName = food[0]
	entryTuple = food[1]
	dictionary = data[0]+ dictionary[:index+1] + "'%s':%s," % \
	(str(entryName), str(entryTuple))+ dictionary[index+1:]
	#writes newdictionary
	file = open("Databases/Final_Databases/FoodDatabase.py", "w")
	file.write(dictionary) 
	
	file.close() 
	#reloads dictionary
	imp.reload(FOOD)


def recursiveSearch(search,searchIndex, start = 0):
	results = []
	if len(searchIndex) == 0:
		return results 
	word = search[start:searchIndex[0]]
	for food in FOOD.dictionary_of_food:
		if word in food.lower():
			results.append([food, FOOD.dictionary_of_food[food]]) 
	newstart = searchIndex.pop(0)
	recursiveSearch(search,searchIndex, newstart+1)


def searching(search,searchIndex, start = 0):
	results = []
	searchIndex.append(len(search))
	searchIndex.insert(0, 0)
	for index in range(len(searchIndex)-1):
		word = search[searchIndex[index]:searchIndex[index+1]]
		word = word.strip()
		for food in FOOD.dictionary_of_food:
			if word in food.lower():
				results.append([food, FOOD.dictionary_of_food[food]]) 
	return results