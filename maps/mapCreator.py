loop = True

fName = raw_input("Name of file to write to: ")
f = open(fName, 'w')

while loop:
	line = raw_input("=> ")

	if line == "q" or line == "Q":
		loop = False
	else:
		result = ""
		split = line.split()
		for e in split:
			if e == "C" or e == "G" or e == "E" or e == "WB":
				pass
			else:
				e = int(e) * 10
			result += e
