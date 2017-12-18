def parameterChange(stars, previousStars, currentParameter, lastOperation):
	#this is an algorithm I created to adjust the curviture of the utiltiy curve
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