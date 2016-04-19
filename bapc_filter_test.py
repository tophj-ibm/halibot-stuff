import unittest

import bapc_filter


def test_cases(file):
	cases = []
	with open(file, 'r') as f:
		for line in f:
			expect = True if line[0:1] == "y" else False
			test = line[2:-1]
			cases.append((test, expect))
	return cases


class TestGeneratedRules(unittest.TestCase):

	def test_generateds(self):
		str = ""
		with open("ex.txt", 'r') as f:
			str = f.read()[:-1]  # get rid of last newline
		(name, clauses) = bapc_filter.parse_command(str)

		cases = test_cases("monitors_samples.txt")
		for (case, expect) in cases:
			print(case)
			self.assertEqual(bapc_filter.execute(clauses, case), expect)

if __name__ == '__main__':
	unittest.main()
