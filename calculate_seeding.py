import data_loader
from helper_functions import *

patents, cutoffs, references, max_pat_id = data_loader.loadData()

seed_year = 1998
data = {}
while seed_year > 1975:
	deltas = []
	for diff in range(1, seed_year - 1974):
		tran_year = seed_year - diff

		seed_year_beg = cutoffs[seed_year]
		seed_year_end = cutoffs[seed_year + 1]
		tran_year_beg = cutoffs[tran_year]
		tran_year_end = cutoffs[tran_year + 1]

		seed_year_val = 0
		tran_year_val = 0
		init_val = 1

		for reference in references:
			pat_id = reference[0]
			refs = reference[1]
			if pat_id >= seed_year_beg and pat_id < seed_year_end:
				seed_year_val += init_val
				tran_val = float(init_val) / patents[pat_id]["deg"]
				for ref_pat_id in refs:
					if ref_pat_id >= tran_year_beg and ref_pat_id < tran_year_end:
						tran_year_val += tran_val
			elif pat_id < seed_year_beg:
				break

		deltas.append(tran_year_val / seed_year_val)

	data[seed_year] = list(deltas)
	print str(seed_year) + ": " + ", ".join(["%.4f" % delta for delta in deltas])

	seed_year -= 1

with open("output.txt", "wb") as file:
	keys = reversed(sorted(data.keys()))
	for key in keys:
		file.write("\t".join(["%.4f" % delta for delta in data[key]]) + "\n")