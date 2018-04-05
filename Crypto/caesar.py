def char_to_int(char):
	return ord(char)-96

def int_to_char(num):
	return chr((num%26)+96)

text = "the quick brown fox jumped over the lazy dog"
res = []

for i in range(1, 27):
	current = ""
	for char in text:
		#check for actual letter
		if (ord(char) > 64 and ord(char) < 91) or (ord(char) > 96 and ord(char) < 122):
			shifted = int_to_char(char_to_int(char) + i)
		else:
			shifted = char
		current += shifted
	res.append(current)


file = open("/usr/share/dict/british-english")
words = file.read().split("\n")
file.close()
i=0
for result in res:
	i += 1
	current = ""
	for word in result.split(" "):
		if word in words:
			current += '\033[92m\033[1m' + word + '\033[0m'
		else:
			current += word
		current += " "
	print(str(i) + ": " + current)
#TODO:
# add command line params
#improve dict with pickle / hash table