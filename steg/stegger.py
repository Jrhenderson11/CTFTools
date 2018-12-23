import os
import numpy
from collections import OrderedDict
from PIL import Image, ImageFile

from menuer import Menu

ImageFile.LOAD_TRUNCATED_IMAGES = True

def printgreen(text):
	print('\033[92m' + text + '\033[0m')

def printred(text):
	print('\033[31m' + text + '\033[0m')
# ---- Array Stuff ----

def diff_arrays(arr1, arr2):
	diffed = []

	#xor data to get key
	for i in range(0, len(arr1)):
		if (i%2==0):
			#diffed.append(arr1[i]^arr2[i])
			diffed.append(arr1[i])
		else:
			diffed.append(0)
	return diffed

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

	for i in range(0, len(arr)):
		item = arr[i]
		if (isinstance(item, tuple)):
			item = item[0]
		#might need [0]
		binary = "{0:b}".format(item)
		#pad binary
		while (len(binary)< 8):
			binary = "0"+binary
		for x in range(8):
			if (binary[x]=="1"):
				planes[x].append(255)
			else:
				planes[x].append(0)


	return planes

def save_planes(planes, width, height):
	fname = "plane"
	for i in range(len(planes)):
		fname = "plane" + str(i) + ".bmp"
		new_image = construct_image(planes[i], width, height)
		new_image.save(fname, 'bmp')
		print("Saved " + fname)

# ---- Menu Functions ----

def xor_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = xor_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print("enter output file: (default key.bmp)")
	fname3 = input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def add_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = add_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print("enter output file: (default key.bmp)")
	fname3 = input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def and_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")

	keypix = and_arrays(pix1, pix2)
	new_image = construct_image(keypix, width, height)
	print("enter output file: (default key.bmp)")
	fname3 = input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def sub_images():
	
	(pix1, pix2) = get_2_image_data("image1.bmp", "image2.bmp")
	keypix = sub_arrays(pix1, pix2)		

	new_image = construct_image(keypix, width, height)
	print("enter output file: (default key.bmp)")
	fname3 = input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def combine_4_images():
	print("enter file: (default qr_part)")
	base = input()
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

	#print(len(array))
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
	print("enter imput file: (default enc1.bmp)")
	fname = input()
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
	print("enter output file: (default key.bmp)")
	fname3 = input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def recombine_planes():
	print("enter file prefix: (default plane)")
	prefix = input()
	if prefix=="":
		prefix = "plane"

	print("enter file suffix: (default .bmp)")
	suffix = input()
	if suffix=="":
		suffix = ".bmp"


	fname = ""
	planes = ([], [], [], [], [], [], [], [])

	#get pixel data into 8 arrays 
	for i in range(8):
		fname = prefix + str(i) + suffix
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

	#print(len(array))
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
	print("enter first file: (default image.png)")
	fname = input()
	if fname=="":
		fname = "image.png"

	image1 = Image.open(fname, 'r')
	
	pixels = image1.load()
	
	width, height = image1.size
	#load pixel data into array
	pix1 = []
	
	for x in range(width):
		for y in range(height):
			cpixel = pixels[x, y]
			pix1.append(cpixel)
	planes = bit_planes(pix1)
	save_planes(planes, width, height)

def extract_bytes():
	print("width first? y/n")
	ans = input().lower()	
	while ans != "y" and ans != "n":
		ans = input().lower()

	data = get_image_data("image.png", width_first=(ans=="y"))
	print("enter output file: (default output)")
	fname = input()
	if fname=="":
		fname = "output"
	f = open(fname, "wb")
	for l in data:
		for x in l:
			f.write(bytes([x]))
	f.close()

def dither():
	printred("not working yet :p")

# ---- Image IO ----

def get_image_data(default, width_first=True):
	print("enter first file: (default " + default + ")")
	fname = input()
	if fname=="":
		fname = default

	image = Image.open(fname, 'r')

	pixels = image.load()
	
	width, height = image.size
	
	pix = []
	if width_first:
		for x in range(width):
			for y in range(height):
				pix.append(pixels[x, y])
	else:
		for y in range(height):
			for x in range(width):
				pix.append(pixels[y, x])
	return pix

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
		   # print(cpixel)

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

	for i in range(len(array)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = array[i]
	return new_image

def save_image(image):
	print("enter output file: (default result.bmp)")
	fname = input()
	if fname=="":
		fname = "result.bmp"
	image.save(fname)


if __name__ == '__main__':

	asciiart = """\033[1m\033[93m	   _____ __            
	  / ___// /____  ____ _____ ____  _____
	  \__ \/ __/ _ \/ __ `/ __ `/ _ \/ ___/
	 ___/ / /_/  __/ /_/ / /_/ /  __/ /    
	/____/\__/\___/\__, /\__, /\___/_/     
	              /____//____/             \033[0m\n"""

	menu_items = OrderedDict([("XOR 2 images",xor_images)
	,("AND 2 images",and_images)
	,("ADD 2 images",add_images)
	,("SUB 2 images",sub_images)
	,("XOR 2 images",xor_images)
	,("Split into planes",get_planes)
	,("Recombine planes",recombine_planes)
	,("Dither",dither)
	,("Extract bytes", extract_bytes)])


	try:
		m = Menu(asciiart, menu_items, tab="	   	")
		m.menu_loop()
	except KeyboardInterrupt as e:
		printred("quitting")

#TODO: 
# interpret args
# ls
# side ls
# minimal
