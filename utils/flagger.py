#!/usr/bin/python3
import re
import string
import argparse
from colorama import Fore, Style


class Sorter():

	dictionary = None

	def deleet(self, word):
		# Get it?
		l337 = {'1':'l', '3':'e', '4':'a', '5':'s', '7':'t', '8':'b', '9':'g'}
		for char in l337:
			word.replace(char, l337[char])
		return word

	# TODO: measure words as minimum edit distance between any word in dictionary (copes with mistakes and unknown punctuation better)
	def flag_like(self, input):
		# Returns how likely a input of chars without an intro or {} is to be a flag
		# basically sees if it is a sequence of english words and _
		score = 0.0
		
		# Load an english dictionary
		if self.dictionary is None:
			with open('/usr/share/dict/british-english') as file:
				self.dictionary = file.read().split("\n")

			# preprocess dictionary to accept things without punctuation
			for word in self.dictionary:
				for char in string.punctuation:
					if char in word:
						self.dictionary.append(word.replace(char, ""))

			self.dictionary.append(self.intro)

		words = input.split("_")
		socre = sum([1 for word in words if self.deleet(word).lower() in self.dictionary])
		# normalise
		score = score / len(words)
		return score

	def sort_text(self, strings):

		sanitised = []

		for item in strings:
			# Remove flag{} characters
			original = item
			item = item.replace(self.intro, "")
			if re.match("^\{.*}$", item) is not None:
				item = item[1:-1]
			sanitised.append((original, self.flag_like(item)))
		
		return [x[0] for x in sorted(sanitised, key=lambda x: x[1], reverse=True)]

	def sort(self, data):

		# Discard non printable items
		data = [item for item in data if item.strip() !="" and ["x" for c in item if c not in string.printable]==[]]

		# split input into categories depending on regex matching
		perfect, bracketed, with_intro, rest = [], [], [], []

		for item in data:
			if re.match(("^"+self.intro+"\{.*\}$"), item) is not None:
				perfect.append(item)
			elif re.match("^\{.*}$", item) is not None or re.match("^.*}$", item) is not None or re.match("^\{.*$", item) is not None:
				bracketed.append(item)
			elif self.intro in item:
				with_intro.append(item)
			else:
				rest.append(item)
		
		return self.sort_text(perfect) + (self.sort_text(bracketed)) + (self.sort_text(with_intro)) + (self.sort_text(rest))
	
	def sort_and_display(self, data):
		if ("\n" in data):
			print("\n".join(self.sort(data.split("\n"))))

	def process_stream(self):
		# Continuously accepts input, terminated with newlines and tries to highlight flag-like strings
		try:
			while True:
				data = input()
				matches = re.findall("(("+self.intro+")?(\{)?([A-z0-9]+_)([A-z0-9]+)+(\})?)", data)
				if len(matches) > 0:
					print(data.replace(matches[0][0], (Fore.GREEN + Style.BRIGHT + matches[0][0] + Fore.RESET + Style.NORMAL)))
				else:
					print(data)
		except (KeyboardInterrupt, EOFError):
			print(Fore.RED + Style.BRIGHT + "Input over" + Fore.RESET + Style.NORMAL)
			exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="CTF flag detector")
	parser.add_argument("filename", help="file path to use as input", nargs="?")
	parser.add_argument("--intro", help="string to replace flag in flag\{\}", default="flag")

	args = parser.parse_args()
	filename = args.filename

	Sorter.intro = args.intro

	if filename != None and filename != "":
		try:
			with open(filename, "r") as f:
				data = f.read()
		except FileNotFoundError:
			print(Fore.RED + Style.BRIGHT + "File not found" + Fore.RESET + Style.NORMAL)
			exit(-1)
		Sorter().sort_and_display(data)
	else:
		Sorter().process_stream()
