import os
import numpy
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def printgreen(text):
	print '\033[92m' + text + '\033[0m'

def printred(text):
	print '\033[31m' + text + '\033[0m'

def print_intro():
	print("\033[1m\033[93m")
	print("   _____ __                            ")
	print("  / ___// /____  ____  ____  ___  _____")
	print("  \__ \/ __/ _ \/ __ `/ __ `/ _ \/ ___/")
	print(" ___/ / /_/  __/ /_/ / /_/ /  __/ /    ")
	print("/____/\__/\___/\__, /\__, /\___/_/     ")
	print("              /____//____/             ")
	print("\033[0m")

def print_menu_items():
	#print "\nMenu:"
	print "	[1] XOR 2 images"
	print "	[2] AND 2 images"
	print "	[3] ADD 2 images"
	print "	[4] SUB 2 images"
	print "	[5] Split into planes"
	print "	[6] Recombine planes"
	print "	[7] Dither\n"

def menu():
	os.system("clear")
	print_intro()
	print "\n"	
	print_menu_items()
	num = int(raw_input())
	while not (num>0 and num<8):
		os.system("clear")
		print_intro()
		print "	   \033[31m\033[1m  invalid input \033[0m\n"
		print_menu_items()
		num = int(raw_input())

	if (num==1):
		xor_images()
	elif (num==2):
		and_planes()
	elif (num==3):
		add_images()
	elif (num==4):
		and_images()
	elif (num==5):
		save_planes()
	elif (num==6):
		recombine_planes()
	elif (num==7):
		dither()

# ---- Array Stuff ----

def diff_arrays(arr1, arr2):
	xord = []

	#xor data to get key
	for i in range(0, len(arr1)):
		if (i%2==0):
			#xord.append(arr1[i]^arr2[i])
			xord.append(arr1[i])
		else:
			xord.append(0)
	return xord

def xor_arrays(arr1, arr2):
	
	xord = []

	#xor data to get key
	for i in range(0, len(arr1)):
		item1 = arr1[i]
		item2 = arr2[i]
		if (isinstance(item1, tuple)):
			item1 = item1[0]
		if (isinstance(item2, tuple)):
			item2 = item2[0]

		xord.append(item1^item2)
	return xord

def sub_arrays(arr1, arr2):

	subd = []
	for i in range(len(arr1)):
		item1 = arr1[i]
		item2 = arr2[i]
		if (isinstance(item1, tuple)):
			item1 = item1[0]
		if (isinstance(item2, tuple)):
			item2 = item2[0]
		subd.append(abs(item1-item2))
	return subd

def and_arrays(arr1, arr2):
	anded = []

	#xor data to get key
	for i in range(0, len(arr1)):

		item1 = arr1[i]
		item2 = arr2[i]
		if (isinstance(item1, tuple)):
			item1 = item1[0]
		if (isinstance(item2, tuple)):
			item2 = item2[0]

		anded.append(item1&item2)
	return anded

# ---- Bit Planing ----

def bit_planes(arr):
	planes = ([], [], [], [], [], [], [], [])

	#xor data to get key
	for i in range(0, len(arr)):
		item = arr[i]
		if (isinstance(item, tuple)):
			item = item[0]
		#might need [0]
		binary = "{0:b}".format(item)
		#pad binary
		while (len(binary)< 8):
			binary = "0"+binary
		#print binary
		for x in range(8):
			if (binary[x]=="1"):
				planes[x].append(255)
			else:
				planes[x].append(0)


	return planes

def save_planes(planes):
	fname = "plane"
	for i in range(len(planes)):
		fname = "plane" + str(i) + ".bmp"
		new_image = construct_image(planes[i], 512, 512)
		new_image.save(fname, 'bmp')

# ---- Menu Functions ----

def xor_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = xor_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def add_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = add_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def and_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")

	#keypix = xor_bmp_tif(pix1, pix2)
	keypix = and_arrays(pix1, pix2)
	new_image = construct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def sub_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = sub_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def combine_4_images():
	print "enter file: (default qr_part)"
	base = raw_input()
	if base=="":
		base = "qr_part"
	planes = ([], [], [], [], [], [], [], [])

	#get pixel data into 8 arrays 
	for i in range(8):
		fname = base + str(i) + ".bmp"
		#open image
		image = Image.open(fname, 'r')
		pixels = image.load()
		
		for x in range(512):
			for y in range(512):
				cpixel = pixels[x, y]


	#reconstruct planes
	width = 512
	height = 512
	new_image = Image.new('RGB', (512, 512))
	data = new_image.load()

	#print len(array)
	for i in range(len(planes[0])):
		binstring = ""
		for x in range(8):
			binstring = binstring + str(planes[x][i])

		#binstring is complete

		val = int(binstring, 2)

		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = val
	
	save_image(new_image)

def xor_one_image(val):
	print "enter imput file: (default enc1.bmp)"
	fname = raw_input()
	if fname=="":
		fname = "enc1.bmp"
	image1 = Image.open(fname, 'r')

	pixels = image1.load()
	width, height = image1.size
	#load pixel data into array
	pix1 = []
	for x in range(width):
		for y in range(height):
			cpixel = pixels[x, y]
			pix1.append(cpixel)

	pix2 = []
	for x in range(width):
		for y in range(height):
			pix2.append(val)
	keypix = xor_arrays(pix1, pix2)
	new_image = construct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def recombine_planes():
	fname = ""
	planes = ([], [], [], [], [], [], [], [])

	#get pixel data into 8 arrays 
	for i in range(8):
		fname = "xor" + str(i) + ".bmp"
		#open image
		image = Image.open(fname, 'r')
		pixels = image.load()
		for x in range(512):
			for y in range(512):
				cpixel = pixels[x, y]
				if cpixel[0]==255:
					planes[i].append(1)
				else:
					planes[i].append(0)

	#reconstruct planes
	width = 512
	height = 512
	new_image = Image.new('RGB', (512, 512))
	data = new_image.load()

	#print len(array)
	for i in range(len(planes[0])):
		binstring = ""
		for x in range(8):
			binstring = binstring + str(planes[x][i])

		#binstring is complete

		val = int(binstring, 2)

		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = val
	
	save_image(new_image)

def get_planes():
	print "enter first file: (default lena.tif)"
	fname = raw_input()
	if fname=="":
		fname = "lena.tif"

	image1 = Image.open(fname, 'r')
	
	pixels = image1.load()
	
	width, height = image1.size
	#load pixel data into array
	pix1 = []
	
	for x in range(width):
		for y in range(height):
			cpixel = pixels[x, y]
			pix1.append(cpixel)
		   # print cpixel
	planes = bit_planes(pix1)
	save_planes(planes)

def dither():
	print("not working yet :p") 

# ---- Image IO ----

def get_2_image_data(default1, default2):
	print "enter first file: (default " + default1 + ")"
	fname = raw_input()
	if fname=="":
		fname = default1
	print "enter second file: (default " + default1 + ")"
	fname2 = raw_input()
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

def construct_image(array, width, height):
	#reassemble key image
	
	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	print len(array)
	for i in range(len(array)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = array[i]
	return new_image

def save_image(image):
	print("enter output file: (default result.bmp)")
	fname = raw_input()
	if fname=="":
		fname = "result.bmp"
	image.save(fname)

try:
	menu()
except KeyboardInterrupt as e:
	printred("quitting")