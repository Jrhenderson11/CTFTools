import os
import numpy
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def print_intro():
	print "       _______"
	print "      /    \\\\\\\\"
	print "     /  /\  \\\\\\\\"
	print "    /  ///\  \\\\\\\\"
	print "   /  //// \__\\\\\\\\"
	print "   \  \\\\\\\\ /  ////"
	print "    \  \\\\\\\\  ////"
	print "     \  \\\\\\\\////"
	print "      \  \\\\\///"
	print "       `''''''"

def menu():
	print_intro()
	print "\nMenu:"
	print "[1] XOR 2 images"
	print "[2] XOR image with white"
	print "[3] XOR image with black"
	print "[4] XOR file\n"
	num = raw_input()
	while not (num>0 and num<5):
		os.system("clear")
		print_intro()
		print "\033[31m	 invalid input \033[0m"
		print "\nMenu:"
		print "[1] XOR 2 images"
		print "[2] XOR image with white"
		print "[3] XOR image with black"
		print "[4] XOR file\n"
		num = raw_input()

	if (num==1):
		xor_images()
	elif (num==2):
		xor_one_image((255,255,255))
	elif (num==3):
		xor_one_image((0,0,0))


def xor_arrays(arr1, arr2):
	xord = []

	#xor data to get key
	for i in range(0, len(arr1)):
		tuple1 = arr1[i]
		tuple2 = arr2[i]
		x = ()
		for i2 in range(0, len(tuple1)):
			xval = tuple1[i2] ^ tuple2[i2]
			x = x + (xval,)
		xord.append(x)
	return xord

def contruct_image(array, width, height):
	#reassemble key image
	
	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	print len(keypix)
	for i in range(len(keypix)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = keypix[i]
	return new_image

def xor_images():
	print "enter first file: (default enc1.bmp)"
	fname = raw_input()
	if fname=="":
		fname = "enc1.bmp"
	print "enter second file: (default enc2.bmp)"
	fname2 = raw_input()
	if fname2=="":
		fname2 = "enc2.bmp"

	image1 = Image.open(fname, 'r')
	image2 = Image.open(fname2, 'r')

	pixels = image1.load()
	pixels2 = image2.load() 
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
	        cpixel = pixels2[x, y]
	        pix2.append(cpixel)

	keypix = xor_arrays(pix1, pix2)
	new_image = contruct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

def xor_one_image(val):
	print "enter first file: (default enc1.bmp)"
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
	new_image = contruct_image(keypix, width, height)
	print "enter output file: (default key.bmp)"
	fname3 = raw_input()
	if fname3=="":
		fname3 = "key.bmp"
	new_image.save(fname3, 'bmp')

menu()