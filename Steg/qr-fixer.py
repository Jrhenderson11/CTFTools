import os
import re
import sys
import math
import numpy
from os import listdir, walk
from os.path import isfile, join
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def printgreen(text):
	print('\033[92m' + text + '\033[0m')

def printred(text):
	print('\033[31m' + text + '\033[0m')

def print_help():
	printgreen("		qr-fixer help menu")
	print('''
		Usage: python3 qr-fixer.py [Options]
		OPTIONS:
		  - help:	unsurprisingly prints this menu
		  - minimal:	doesn't clear screen or display intro art
		''')

def attach_ls(text):

	files = []
	max_length = 0
	for f in listdir("./"):
		if isfile(join("./", f)):
			files.append(f)
			if len(f) > max_length:
				max_length = len(f)

	width = max_length + 4
	lines = text.split("\n")
	offset = 36
	#do top
	lines[0] = lines[0][:offset] +"\033[92m"+"	"*7+ " files:"
	#do 2nd
	lines[1] = "\033[34m" + lines[1][:offset] +"\033[92m "+ "=" * width
	
	#do middle
	for i in range(2, len(lines)-1):
		if lines[i]=="":
			lines[i] = "\033[34m" + lines[i] + "\033[92m"+("	"*6)+ " "*2+ "| " + files[i] + "\033[0m"
		else:
			lines[i] = "\033[34m" + lines[i]+ (" " * (offset-len(lines[i]))) +"\033[92m"+("	"*(4-int(len(lines[i])/4)))+ "| " + files[i] + "\033[0m"

	#do last
	lines[len(lines)-1] = "\033[34m" + lines[len(lines)-1][:offset] +"\033[92m"+"	"*6 + (" " *2)+ "=" * width + "\033[0m"

	for line in lines:
		line = line + "\n"
	return "\n".join(lines)


def print_intro():
	text = '''\033[34m
	         .::::::::    :::::::::  	  	
	        :+:    :+:   :+:    :+: 	
	       +:+    +:+   +:+    +:+  	
	      +#+    +:+   +#++:++#:    	
	     +#+    +#+   +#+    +#+    	
	    #+#    #+#   #+#    #+#     	
	    ########### ###    ###  	   	  \n
\033[1m\033[97m	            -- Fixer --			  \033[0m'''
	return text

def get_menu_text():
	return '''	\033[97m[1] Basic QR reconstruction		  
	\033[97m[2] Convert to black and white		  \n
'''

def menu():
	text = ""
	if not MINIMAL:
		os.system("clear")
		text = print_intro()
		text += "\n\n"	
	text += get_menu_text()
	print(attach_ls(text))
	try:
		i = input()
		num = int(i)
	except ValueError as e:
		if (i=="q"):
			exit()
		num = -1
	while not (num>0 and num<3):
		text = ""
		if not MINIMAL:
			os.system("clear")
			text = print_intro()
		text += "\n         	\033[31m\033[1m  invalid input \033[0m		  \n"
		if not MINIMAL:
			text+=get_menu_text()
		print(attach_ls(text))
		try:
			i = input()
			num = int(i)
		except ValueError as e:
			if (i=="q"):
				exit()
			num = -1

	if (num==1):
		basic_repair()
	if (num==2):
		flatten_image()

# ---- Unclassified Stuff ----
# looks at arguments and does some stuff? 
def interpret_args():
	args = sys.argv[1:]
	#print(args)
	if 'help' in args:
		print_help()
		exit()
	if 'minimal' in args:
		global MINIMAL
		MINIMAL = True

# ---- Main Functions ----
def basic_repair():
	#different qr code versions have different numbers of blocks, one of the common ones is 29
	qr_size = 29

	(pixels, width, height) = get_image_data("qr.png")

	blocks = numpy.zeros((qr_size, qr_size))

	for block_y in range(qr_size):
		for block_x in range(qr_size):

			#something
			colours = [0, 0]
			for small_y in range(int(height/qr_size)):
				for small_x in range(int(height/qr_size)):
					
					x = ((block_x*height/qr_size) + small_x)
					y = ((block_y*height/qr_size) + small_y)

					pixel = 255 * math.floor(pixels[x,y][0]/128)

					#black
					if (pixel == 0):
						colours[1] = colours[1] + 1					
					else:
						colours[0] = colours[0] + 1
			m = 0
			
			#debug	
			#print colours[1]
			#print colours[0]

			if colours[1]>colours[0]:
				blocks[block_x, block_y] = 1
			else:
				blocks[block_x, block_y] = 0

	blocks = overwrite_fixed_patterns(blocks, qr_size)

	qr_image = make_qr_image(blocks, width, height)
	qr_image.show()
	save_image(qr_image)

def overwrite_fixed_patterns(qr_array, qr_size):
	if (qr_size==29):
		
		x=0
		y=0

		#vertical
		for y2 in range(22,29):
			qr_array[0, y2] = 1
			qr_array[6, y2] = 1

		for (x,y) in [(0,0), (22,0), (0,22)]:
			#corner boxes
			#horizontal lines
			for x2 in range(7):
				qr_array[x+x2, y] = 1
				qr_array[x+x2, y+6] = 1
			
			#vertical
			for y2 in range(7):
				qr_array[x, y2] = 1
				qr_array[x+6, y2] = 1

			#centre
			for y2 in range(3):
				for x2 in range(3):
					qr_array[x+2+x2,y+2+y2] = 1
	
			#white outline
			for x2 in [-1, 8]:
				for y2 in [-1, 8]:	
					if ((x+x2) > 0 and (x+x2) < 29) and ((y+y2) > 0 and (y+y2) < 29):
						qr_array[x+x2, y+y2] = 0

		#dotted lines
		for x in range(7, 22):
			if x%2==0:
				qr_array[x, 6]=1
				qr_array[6, x]=1
			else:
				qr_array[x, 6]=0
				qr_array[6, x]=0

		#small alignment square
		for x in range(20, 25):
			qr_array[x,20] = 1
			qr_array[x,24] = 1
			qr_array[20,x] = 1
			qr_array[24,x] = 1
		qr_array[22,22] = 1

	return qr_array

def flatten_image():
	(pixels, width, height) = get_image_data("Lucy.jpg")
	newpixels = numpy.zeros((width, height))
	for x in range(width):
		for y in range(height):
			newval = 255 * math.floor(pixels[x,y][0]/128)
			newpixels[x,y] = newval#, newval, newval)

	image = construct_image_2d(newpixels, width, height)
	image.show()
	save_image(image)

#
# ---- Image IO ----

def get_image_data(default):
	print("enter first file: (default " + default + ")")
	fname = input()
	if fname=="":
		fname = default

	exists = True

	try:
		image = Image.open(fname, 'r')
	except FileNotFoundError as e:
		exists = False

	while (exists==False):
		exists = True
		printred("File " + fname + " not found")
		print("enter first file: (default " + default + ")")
		fname = input()
		if fname=="":
			fname = default		
		try:
			image = Image.open(fname, 'r')
		except FileNotFoundError as e:
			exists = False

	pixels = image.load()
	
	width, height = image.size
	
	#load pixel data into arrays
	return (pixels, width, height)

def make_qr_image(qr_array, width, height):

	qr_image = Image.new('RGB', (width, height))
	pixels = qr_image.load()

	qr_size = len(qr_array[0])
	block_size = width / qr_size

	for block_y in range(qr_size):
		for block_x in range(qr_size):

			#something
			colours = [0, 0]
			for small_y in range(int(height/qr_size)):
				for small_x in range(int(height/qr_size)):
					
					x = ((block_x*height/qr_size) + small_x)
					y = ((block_y*height/qr_size) + small_y)
					block = qr_array[block_x, block_y] 
					pixels[(x, y)] = (255-(255 * int(block)), 255-(255 * int(block)), 255-(255 * int(block))) 

	return qr_image

def construct_image(array, width, height):
	#reassemble key image

	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	print(len(array))
	for i in range(len(array)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = array[i]
	return new_image

def construct_image_2d(array, width, height):

	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	#print(len(array))
	for x in range(width):
		for y in range(height):
			val = array[x, y]
			data[x, y] = int(val), int(val),int(val) 
	return new_image

def save_image(image):
	num = get_num_files("qr_new")
	print("enter output file: (default qr_new"+str(num)+".png)")
	fname = input()
	if fname=="":
		fname = "qr_new"+str(num)+".png"
	image.save(fname)

def get_num_files(base):
	onlyfiles = ""
	for f in listdir("./"):
		if isfile(join("./", f)):
			onlyfiles += " " + f
	#print(str(len(re.findall((base + "\d+\."), onlyfiles))) + " files found called " + base) 
	return len(re.findall((base + "\d+\."), onlyfiles))

global MINIMAL
MINIMAL = False

try:
	interpret_args()
	menu()
except KeyboardInterrupt as e:
	printred("quitting")

#TODO:
# fix overwrite basic
# fix basic
# brute force based on certainty
# input log
# ls command
# side ls
# conf file to configure minimal 
# crop to size
# show lines
# stop showing lines when I don't want them