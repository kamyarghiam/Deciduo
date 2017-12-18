
#this allows for us to change the parameter as a funciton of several factors 
def parameterChange(stars, previousStars, currentParameter, lastOperation):
	#this is an algorithm I created to adjust the curviture of the utiltiy curve
	stars = float(stars)
	previousStars = float(previousStars)
	currentParameter = float(currentParameter)
	maxStars = 5
	if stars == maxStars:
		return [currentParameter, lastOperation]
	if stars == previousStars:
		if lastOperation == "*":
			return [currentParameter*1.1, "*"]
		elif lastOperation == "/":
			return [currentParameter/1.1, "/"]
	elif stars < previousStars:
		if lastOperation == "*":
			return [currentParameter/((previousStars-stars)//5+1), "/"]
		elif lastOperation == "/":
			return [currentParameter*((previousStars-stars)//5+1), "*"]
	else: 
		if lastOperation == "*":
			return [currentParameter*1.1, "*"]
		elif lastOperation == "/":
			return [currentParameter/1.1,"/"]