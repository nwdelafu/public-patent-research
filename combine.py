import sys

class Status():
	def __init__(self, first=0, last=1, prompt=""):
		self.first = first
		self.last = last
		self.range = last - first
		self.curr_p = 0
		self.prompt = prompt

	def print_status(self, now):
		p = (now - self.first) * 100 / self.range
		if p > self.curr_p:
			self.curr_p = p
			print "\r%s%3d%% finished  [%s%s]" % (self.prompt, self.curr_p, "%" * (p / 10), ">" + (" " * (9 - p / 10)) if p < 100 else ""),
			sys.stdout.flush()

	def done(self):
		self.print_status(self.last)
		print ""

references = {}
files = ["reference_data_1975-1999.csv", "reference_data_1976-2006.csv"]
num_of_lines = 16521700 + 23650054
status = Status(0, num_of_lines)
i = 0
for filename in files:
	with open(filename) as file:
		file.readline()
		for line in file:
			tokens = line.strip().split(",")
			citer = int(tokens[0])
			cited = int(tokens[1])

			if citer not in references:
				references[citer] = {}

			if cited not in references[citer]:
				references[citer][cited] = True

			i += 1
			status.print_status(i)
status.done()

lines = ["citing,cited"]
for citer in sorted(references.keys()):
	for cited in sorted(references[citer].keys()):
		lines.append("%d,%d" % (citer, cited))

with open("reference_data_1975-2006.csv", "wb") as file:
	for i in range(0, len(lines)):
		if i < len(lines) - 1:
			file.write(lines[i] + "\n")
		else:
			file.write(lines[i])