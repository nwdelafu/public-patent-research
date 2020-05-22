import sys

def loadData(show_status=True, lines_in_file=16521699):
	patents = {}
	cutoffs = {}
	references = []
	max_pat_id = -1
	i = 0
	curr_p = 0

	print "Loading data"
	with open("data/year_cutoffs.txt") as file:
		for line in file:
			year, first_pat = line.strip().split("\t")
			cutoffs[int(year)] = int(first_pat)

	with open("data/reference_data_detailed.csv") as file:
		file.readline()
		for line in file:
			tokens = line.strip().split(",")

			pat1 = int(tokens[0])
			pat2 = int(tokens[1])
			refs = int(tokens[2])

			if pat1 not in patents:
				patents[pat1] = {}
				patents[pat1]["id"]  = pat1
				patents[pat1]["val"] = 0
				patents[pat1]["deg"] = refs
				references.append((pat1, []))

			references[len(references) - 1][1].append(pat2)

			max_pat_id = max(max_pat_id, pat1)

			if show_status:
				i += 1
				p = i * 100 / lines_in_file
				if p > curr_p:
					curr_p = p
					print "\r%3d%% loaded  [%s%s]" % (curr_p, "%" * (p / 10), ">" + (" " * (9 - p / 10)) if p < 100 else ""),
					sys.stdout.flush()
			if i > lines_in_file:
				break
	print ""
	references.reverse()

	return [patents, cutoffs, references, max_pat_id]