import sys

def char_to_int(char):
	if (ord(char) > 96 and ord(char) < 122):
		return ord(char)-96
	elif (ord(char) > 64 and ord(char) < 91):
		return ord(char)-64

def int_to_char(num):
	if (ord(char) > 96 and ord(char) < 122):
		return chr((num%26)+96)
	elif (ord(char) > 64 and ord(char) < 91):
		return chr((num%26)+64)

text = '''KBJICYP CZ KHLTIKWECD

KHLTIKWECD RWMI GBQW JCNW IBNW BM NHP CZ 2017. JBMLW IKWM, BI KHJ FYCRM QWYP VOBLTGP IC IKCOJHMSJ CZ NWNEWYJ ZYCN HGG CQWY IKW FGCEW.
IKW KHGG CZ ZHNW GBJIJ IKW ICA 100 OJWYJ BM CYSWY CZ ACBMIJ. HI IKW IBNW CZ RYBIBMF, IKW ICA 3 OJWYJ HYW JIWZHMC118, ZBGGBACJ HMS HKNWS.
IKWYW HYW JCNW ZCYONJ, H JKCOIECD HMS H JGHLT LKHMMWG. JGHLT HMS JKCOIECD HYW HRWJCNW, EOI IKW ZCYONJ MWWS JCNW GCQW! B RBJK NCYW AWCAGW OJWS IKWN.
KCAWZOGGP IKBJ BJ WMCOFK IWDI IC KWGA RBIK PCOY JOEJIBIOIBCM! FWI LYHLTBM! AJ SCM'I ZCYFWI IC JOAACYI KHLTIKWECD BZ PCO LHM JAHYW JCNW NCMWP. WQWYP AWMMP KWGAJ!

DCDC - HYYWDWG
ZGHF GCYWNBAJONSCGCYJBIHNWI'''
#text = "asd hggf heep brp tf jr"

if len(sys.argv) > 1:
	text = sys.argv[1]
	print(text)
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
legitmap = dict()
for result in res:
	legit = 0
	i += 1
	current = ""
	for word in result.split(" "):
		if word.lower() in words or word in words:
			current += '\033[92m\033[1m' + word + '\033[0m'
			legit+=1
		else:
			current += word
		current += " "
	current = str(i) + ": " + current
	#print(str(i) + ": " + current)
	if legit in legitmap:
		legitmap[legit].append(current)
	else:
		legitmap[legit] = [current]
print("Results ordered by translation")
for num in legitmap.keys()[::-1]:
	for sent in legitmap[num]:
		print(sent)

#TODO:
# add command line params
#improve dict with pickle / hash table