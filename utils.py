"""
Receives a list of objects and returns the list as a string, built by
calling str() to each object.
"""
def printable(obj_list):
	ret = ""
	for elem in obj_list:
		if (ret != ""):
			ret += ", "
		ret += str(elem)
	return "["+ret+"]"

