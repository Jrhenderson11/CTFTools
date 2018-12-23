#!/usr/bin/python3

import re
import sys
import numpy as np
import matplotlib.pyplot as plt

#return set of all repeated text strings
def get_repetitions(base, text):
	chars = set(text)
	repetitions = set()
	for char in chars:
		if (len(re.findall(base+char, text))>1):
			repetitions.update({base+char} | get_repetitions(base+char, text))
	return repetitions

#get repetitions without intersecting subsets (e.g "abcdabc" returns "abc" not "ab" "bc" "abc")
def get_occluding_repetitions(base, text):
	repetitions = (get_repetitions(base,text))
	return filter(lambda x: x not in " ".join(repetitions - {x}), repetitions)


def display_freq_chart(text):
	freqs = dict()
	for char in set(text):
		freqs[char] = len(re.findall(char, text))	

	x = list(freqs.keys())
	x.sort()

	y = [freqs[letter] for letter in x]
	
	fig, ax = plt.subplots()
	plt.bar(range(len(freqs)), y, align="center")
	ax.set_title("symbol Frequencies")
	ax.set_ylabel("frequency")
	ax.set_xlabel("symbol")
	plt.xticks(range(len(freqs)), x)
	plt.yticks(range(max(freqs.values())+1))
	plt.show()

if __name__ == '__main__':
	text = "efgggaaaabbbccd"
	if len(sys.argv) >1:
		text = sys.argv[1]
	print("chars: " + str(list(filter(lambda x: len(x)!=1, get_repetitions("", text)))))
	display_freq_chart(text)

#TODO:
#display
#freq (graph?)