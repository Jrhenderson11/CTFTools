#!/usr/bin/python3
import argparse
from ctfutils.englisher import Englisher

class Caesar():

	def rotate(self, letter, rot):
		shift = 97 if letter.islower() else 65
		return chr((ord(letter) + rot - shift) % 26 + shift)

	def apply_caesar(self, data, rot):
		current = ""
		for char in data:
			if (ord(char) > 64 and ord(char) < 91) or (ord(char) > 96 and ord(char) < 122):
				shifted = self.rotate(char, rot)
			else:
				shifted = char
			current += shifted
		return current

	def brute_force(self, data):
		e = Englisher()
		for x in [(i, self.apply_caesar(data, i)) for i in range(1, 27)]:
			print(str(x[0]) + ": " + e.highlight_english(x[1]))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Caesar cipher solver")
	parser.add_argument("input", help="String to brute force")
	Caesar().brute_force(parser.parse_args().input)