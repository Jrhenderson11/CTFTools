#!/usr/bin/python3
from colorama import Fore, Style

RESET = Fore.RESET+ Style.NORMAL
BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
BRIGHT_RED = Fore.RED + Style.BRIGHT

class Englisher():

	words = None

	def load_dictionary(self):
		with open("/usr/share/dict/british-english") as f:
			self.words = f.read().split("\n")

	def in_dict(self, word):
		if self.words is None:
			self.load_dictionary()
		return word.lower() in self.words or word in self.words

	def highlight_english(self, data):
		current = ""
		for word in data.split(" "):
			if self.in_dict(word):
				current += BRIGHT_GREEN + word + RESET
			else:
				current += word
			current += " "
		return current

	def get_score(self, data):
		# Generates a score for how many english words a text contains
		return sum([1 for word in data.split(" ") if self.in_dict(word)])

	def sort(self, data):
		scored = [(item, self.get_score(item)) for item in data]
		return [x[0] for x in sorted(scored, key=lambda x: x[1])]

if __name__ == "__main__":
	# Assume if someone is piping input they want it highlighted
	e = Englisher()
	try:
		while True:
			print(e.highlight_english(input()))
	except (KeyboardInterrupt, EOFError):
		print(BRIGHT_RED + "Input over" + RESET)
		exit(0)