def leetspeak(word):
	if word =="":
		return []
	
	subs = []
	#start with e's and a's (most common substitutions)
	wholedict = {'a':4, 'e':3, 'l':1, 'o':0, 's':5, 't':7, 'i':1}
	#AE
	#G?
	#I
	#L
	#0
	#s
	#t
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
	case_sensitive = False

	file = open("rockyou-withcount.txt", 'r')
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
#	file = open("files/patterns.txt", 'w+')
#	file.write("")
#	file.close()

def analyse_numbers():
	import re
	
	file = open("rockyou.txt", 'r')
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
	file = open("files/numbers.txt", 'w+')
	file.write("")
	file.writelines(nums)
	file.close()	

def combine(words, dates):
	#common=word + num
	return



def main():
	analyse_patterns()

main()
