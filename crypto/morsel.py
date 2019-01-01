#!/usr/bin/python3
import argparse
from colorama import Fore, Style

RESET = Fore.RESET+ Style.NORMAL
BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
BRIGHT_RED = Fore.RED + Style.BRIGHT

class Morse():
	morse = {'..-.' : 'F', '-..-' : 'X',
			 '.--.' : 'P', '-'    : 'T', '..---': '2',
			 '....-': '4', '-----': '0', '--...': '7',
			 '...-' : 'V', '-.-.' : 'C', '.'    : 'E', '.---': 'J',
			 '---'  : 'O', '-.-'  : 'K', '----.': '9', '..'  : 'I',
			 '.-..' : 'L', '.....': '5', '...--': '3', '-.--': 'Y',
			 '-....': '6', '.--'  : 'W', '....' : 'H', '-.'  : 'N', '.-.' : 'R',
			 '-...' : 'B', '---..': '8', '--..' : 'Z', '-..' : 'D', '--.-': 'Q',
			 '--.'  : 'G', '--'   : 'M', '..-'  : 'U', '.-'  : 'A', '...' : 'S', '.----': '1'}

	def from_morse(self, symbol):
		if symbol in self.morse:
			return self.morse[symbol]
		else:
			return BRIGHT_RED + symbol + RESET

	def to_morse(self, letter):
		flipped = {self.morse[symbol]:symbol for symbol in self.morse}
		if letter in flipped:
			return flipped[letter.upper()]
		else:
			return BRIGHT_RED + letter + RESET

	def decode(self, data):
		return "".join([self.from_morse(symbol) for symbol in data.split(" ")])

	def encode(self, data):
		return " ".join([self.to_morse(symbol) for symbol in data])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Caesar cipher solver")
	parser.add_argument("mode", help="decode or encode", choices=["encode","decode"])
	args = parser.parse_args()
	m = Morse()
	try:
		while True:
			data = input()
			if args.mode=="encode":
				print(m.encode(data))
			else:
				print(m.decode(data))
	except (KeyboardInterrupt, EOFError):
		print(BRIGHT_RED + "Input over" + RESET)
		exit(0)
