import os
import re
import numpy
from os import listdir, walk
from os.path import isfile, join
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def printgreen(text):
	print('\033[92m' + text + '\033[0m')

def printred(text):
	print('\033[31m' + text + '\033[0m')

def print_intro():
	print("\033[34m")
	print("           .::::::::    ::::::::: ")
	print("          :+:    :+:   :+:    :+: ")
	print("         +:+    +:+   +:+    +:+  ")
	print("        +#+    +:+   +#++:++#:    ")
	print("       +#+    +#+   +#+    +#+    ")
	print("      #+#    #+#   #+#    #+#     ")
	print("      ########### ###    ###      \n")
	print("\033[1m\033[97m            -- Fixer --\033[0m")

def print_menu_items():
	print("	[1] Basic QR reconstruction\n")

def menu():
	os.system("clear")
	print_intro()
	print("\n")	
	print_menu_items()
	num = int(input())
	while not (num>0 and num<2):
		os.system("clear")
		print_intro()
		print("         \033[31m\033[1m  invalid input \033[0m\n")
		print_menu_items()
		num = int(input())

	if (num==1):
		basic_repair()

# ---- Main Functions ----

def basic_repair():
	#different qr code versions have different numbers of blocks, on eof the common ones is29
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

					pixel = pixels[x, y] 

					#debug
					#print pixel

					if (pixel == (0,0,0,255)):
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

	qr_image = make_qr_image(blocks, width, height)
	#qr_image.show()
	save_image(qr_image)

# ---- Image IO ----

def get_2_image_data(default1, default2):
	print("enter first file: (default " + default1 + ")")
	fname = input()
	if fname=="":
		fname = default1
	print("enter second file: (default " + default1 + ")")
	fname2 = input()
	if fname2=="":
		fname2 = default2

	image1 = Image.open(fname, 'r')
	image2 = Image.open(fname2, 'r')

	pixels = image1.load()
	
	pixels2 = image2.load() 
	width, height = image1.size
	
	#load pixel data into arrays
	pix1 = []
	
	for x in range(width):
		for y in range(height):
			cpixel = pixels[x, y]
			pix1.append(cpixel)
		   # print cpixel

	pix2 = []
	for x in range(width):
		for y in range(height):
			cpixel = pixels2[x, y]
			pix2.append(cpixel)

	return (pix1, pix2)

def get_image_data(default):
	print("enter first file: (default " + default + ")")
	fname = input()
	if fname=="":
		fname = default

	image = Image.open(fname, 'r')
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
					pixels[(x, y)] = int(block)

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

try:
	menu()
except KeyboardInterrupt as e:
	printred("quitting")