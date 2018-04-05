

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
	print(str(i) + ": " + current)
