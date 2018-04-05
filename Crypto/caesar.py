def char_to_int(char):
	return ord(char)-96

def int_to_char(num):
	return chr((num%26)+96)

text = "apple"
res = []

for i in range(1, 27):
	current = ""
	for char in text:
		shifted = int_to_char(char_to_int(char) + i)
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