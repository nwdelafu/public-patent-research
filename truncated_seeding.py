import data_loader
from helper_functions import *

patents, cutoffs, references, max_pat_id = data_loader.loadData()

while True:
	year_str = "not an int"
	while not isInt(year_str):
		year_str = raw_input("Enter the truncation year (or \"quit\"): ")
		if year_str == "quit":
			kill()
	year = int(year_str)
	cutoff_patent = cutoffs[year + 1] if year + 1 in cutoffs else max_pat_id
	cohort_patent = cutoffs[year] if year in cutoffs else 1

	seedAndComputeValues(patents, references, cutoff_patent, cohort_patent,
						 seeding.latestCohort, transmission.default, transmission.defaultOut)
	outputPatents(patents, True, cutoff_patent)
