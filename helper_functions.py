import os, re, sys


class seeding:
	@staticmethod
	def default(patent, cohort_patent):
		return 1

	@staticmethod
	def latestCohort(patent, cohort_patent):
		return 1 if patent["id"] >= cohort_patent else 0

class transmission:
	@staticmethod
	def default(patent, cohort_patent):
		return float(patent["val"]) / patent["deg"]

	@staticmethod
	def degreeWeighted(patent, cohort_patent):
		return float(patent["val"]) / (patent["deg"] + 1)

	@staticmethod
	def defaultOut(patent, cohort_patent):
		return 0

	@staticmethod
	def degreeWeightedOut(patent, cohort_patent):
		return float(patent["val"]) * (patent["deg"] - 1) / patent["deg"]

def seedPatents(patents, eval_function, cutoff_patent, cohort_patent):
	for pat_id in patents:
		if pat_id > cutoff_patent:
			patents[pat_id]["val"] = 0
		else:
			patents[pat_id]["val"] = eval_function(patents[pat_id], cohort_patent)

def seedAndComputeValues(patents, references,
						 cutoff_patent, cohort_patent,
						 seed_function=seeding.default,
						 trans_function=transmission.default,
						 trans_loss_function=transmission.defaultOut):
	seedPatents(patents, seed_function, cutoff_patent, cohort_patent)

	for reference in references:
		if reference[0] <= cutoff_patent:
			if len(reference[1]) > 0:
				trans_val = trans_function(patents[reference[0]], cohort_patent)
				for pat_id in reference[1]:
					if pat_id in patents:
						patents[pat_id]["val"] += trans_val
				patents[reference[0]]["val"] -= trans_loss_function(patents[reference[0]], cohort_patent)

def isInt(str):
	try:
		int(str)
		return True
	except Exception:
		return False

def getNextFileIter(fileBaseName="value_"):
	iter = -1
	files = os.listdir("data/")
	p = re.compile(fileBaseName + "(\d+).csv")
	for file in files:
		if p.match(file):
			iter = max(iter, int(p.match(file).group(1)))
	return iter + 1

def compareFloats(a, b):
	return -1 if a < b else 1 if a > b else 0

def getSortedPatentIndices(patents, cutoff_patent):
	indices = sorted(patents.keys())
	if cutoff_patent:
		indices = [p for p in indices if p <= cutoff_patent]
	return sorted(indices, lambda a, b: compareFloats(patents[b]["val"], patents[a]["val"]))

def outputPatents(patents, sorted, cutoff_patent, fileBaseName="value_"):
	filename = "data/" + fileBaseName + str(getNextFileIter(fileBaseName)) + ".csv"
	indices = getSortedPatentIndices(patents, cutoff_patent) if sorted else sorted(patents.keys())
	with open(filename, "wb") as outfile:
		for pat_id in indices:
			outfile.write("%d,%.4f\n" % (pat_id, patents[pat_id]["val"]))

def kill():
	sys.exit()