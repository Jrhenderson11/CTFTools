#generate reverse dict for sorting
#ie a dict with numbers as keys and patterns as values
#this is useful for counting and sorting stuff
def reverse_dict(dictionary):
	revdict = {}
	for key in dictionary:
		if dictionary[key] in revdict:
			revdict[dictionary[key]].append(key)
		else:
			revdict[dictionary[key]] = [key]
	return revdict

#generates leetpeak versions of a word
def leetspeak(word):
	if word =="":
		return []
	
	subs = []
	#start with e's and a's (most common substitutions)
	wholedict = {'a':4, 'e':3, 'l':1, 'o':0, 's':5, 't':7, 'i':1}
	
	letter = word[0]
	words = leetspeak(word[1:])
	if words ==[]:
		subs.append(letter)
		if letter in wholedict:
			subs.append(str(wholedict[letter]))
	else:
		for w in words:
			w1 = letter + w
			if not w1 in subs:
				subs.append(w1)
			if letter in wholedict:
				w2 = str(wholedict[letter]) + w
				subs.append(w2)
			
	return subs

def analyse_patterns():
	import re
	
	#ignoring passwords that are unique saves a lot of time, set to true to ignore anything with count 1
	ignore1 = False
	#decide to generate patterns that distinguish between uppercase and lowercase characters
	case_sensitive = False

	file = open(fname, 'r')
	words = file.read().split("\n")
	file.close()

	numdict = {}

	for word in words:
		#print word.strip()
		count = word.strip().split(" ")[0]
		if ignore1==True and count==1:
			break
		try:
			pattern = word.strip().split(" ")[1]
			if not case_sensitive:
				pattern = re.sub("[a-zA-Z]", "C", pattern)
				pattern = re.sub("[0-9]", "D", pattern)
			else:
				pattern = re.sub("[a-z]", "c", pattern)
				pattern = re.sub("[A-Z]", "C", pattern)
				pattern = re.sub("[0-9]", "D", pattern)		
			print pattern

			if pattern in numdict:
				numdict[pattern] = numdict[pattern] + int(count)
			else:
				numdict[pattern] = int(count)
		except Exception as e:
			pass

	print numdict 

	revdict = reverse_dict(numdict)
	nums = revdict.keys()
	nums.sort(reverse =True)
	text=""
	for num in nums:
		for pattern in revdict[num]:
			line = str(num) + " " + pattern 
		#	print line
			text = text + line + "\n"


	file = open("files/patterns.txt", 'w+')
	file.write(text)
	file.close()


	# TODO: symbols

#finds the most common numbers put at the end of passwords
def analyse_numbers(fname):
	import re
	
	outputfile = "files/numbers.txt"

	file = open(fname, 'r')
	text = file.read()
	file.close()

	regex  = re.compile(r'[^0-9\n\s]+[0-9]+\n')
	numregex = re.compile(r'[0-9]+')
	numwords = re.findall(regex, text)
	nums = []
	found = {}
	
	print len(numwords)
	#raw_input()
	i=0.0
	for word in numwords:
		print word.strip()
		num = re.findall(numregex, word)[0]
		if not num in found:
			found[num] = True
			nums.append(num+"\n")
		
		print num
		i=i+1.0
		percent = (100.0*i) / float(len(numwords)) 
		print str(percent) + "%"

	file = open(outputfile, 'w+')
	file.write("")
	file.writelines(nums)
	file.close()

#actually takes into account the recorded number of times number combination was used
def analyse_numbers_advanced(fname):
	import re
	
	outputfile = "files/numbers-500.txt"

	file = open(fname, 'r')
	text = file.read()
	file.close()

	regex  = re.compile(r'[^0-9\n\s]+[0-9]+\n')
	regex2  = re.compile(r'[^0-9\n\s]+[0-9]+$')
	numregex = re.compile(r'[0-9]+$')
	startnumregex = re.compile(r'^[0-9]+')
	#numwords = re.findall(regex, text)
	nums = []
	found = {}
	numdict = {}
	
	print "working"
	for line in text.split('\n'):
		matches = re.findall(regex2, line)
		#has pattern
		if not matches == []:
			#numwords.append(matches[0])
			#extract num
			word = matches[0]
			num = re.findall(numregex, word)[0]
			try:
				count = re.findall(startnumregex, line.strip())[0]
			except Exception as e:
				print line

				raw_input()
			if num in numdict:
				numdict[num] = numdict[num] + int(count)
			else:
				numdict[num] = int(count)

	#sort numdict with reversing method
	print "sorting"
	revdict = reverse_dict(numdict)
	nums = revdict.keys()
	nums.sort(reverse=True)
	text=""
	print "writing"
	for num in nums[:500]:
		for pattern in revdict[num]:
			line = str(num) + " " + pattern 
		#	print line
			text = text + line + "\n"

	file = open(outputfile, 'w+')
	file.write(text)
	file.close()
	print "written to " + 

#combines possible pieces of information into possible passwords
def combine(words, dates):
	#common=word + num
	return



def main():
	rockyou = "files/rockyou.txt"
	rockyoucount = "files/rockyou-withcount.txt"	
	analyse_numbers_advanced(rockyoucount)
	#analyse_patterns()

main()
