#!/usr/bin/python3

import argparse

class Vignere():

	def __init__(self, key):
		self.key = key

	def set_key(self, key):
		self.key = key

	def rotate(self, letter, rot):
		shift = 97 if letter.islower() else 65
		return chr((ord(letter) + rot - shift) % 26 + shift)

	def apply_cipher(self, data, encode=False):
		if not isinstance(data, str):
			raise TypeError("Cannot decode non string types")
		output = []
		for i, char in enumerate(data):
			keychr = self.key[i%len(self.key)].lower()
			rot = ord(keychr) - 96
			if not encode:
				rot = 0-rot
			output.append(self.rotate(char, rot))
		return "".join(output)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Vignere cipher solver")
	parser.add_argument("input", help="input string", nargs="?")
	parser.add_argument("--key", help="encryption / decryption key", required=True)
	parser.add_argument("--encode", help="encode instead of decode", required=False, action='store_true')

	args = parser.parse_args()
	
	if args.input is None or args.input == "":
		data = input("Enter input string: ")
		print(data)
	else:
		data = args.input
	
	v = Vignere(args.key)
	print(v.apply_cipher(data, encode=args.encode))
