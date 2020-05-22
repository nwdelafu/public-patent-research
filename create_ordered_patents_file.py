data = {}

with open("data/reference_data_stripped.txt") as file:
	file.readline()
	for line in file:
		pat1, pat2 = [int(d) for d in line.split("\t")]
		if pat1 not in data:
			data[pat1] = -1
		if pat2 not in data:
			data[pat2] = -1

print "done in"

sorted_pats = sorted(data.keys())

with open("data/ordered_patents.txt", "wb") as outfile:
	for pat in sorted_pats:
		outfile.write(str(pat) + "\n")