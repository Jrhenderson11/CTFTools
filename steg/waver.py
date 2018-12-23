import os
import re
import wave
import numpy
import wave, struct, math
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def print_intro():
	printblue(" WAVER")
	print("   ____")
	print("  /\___\\")
	print(" /\ \___\\")
	print(" \ \/ / /")
	print("  \/_/_/\n")

def menu():
	print_intro()
	print("\nMenu:")
	print("[1] encode (NOT WORKING YET)")
	print("[2] decode\n")
	num = int(input())
	while not (num>0 and num<5):
		os.system("clear")
		print_intro()
		print("\033[31m  invalid input \033[0m")
		print("\nMenu:")
		print("[1] encode (NOT WORKING YET)")
		print("[2] decode\n")
		num = input()

	if (num==1):
		data = get_wav_data()	
		image = contruct_image(data, 1617, 300)
		save_image(image)
	elif (num==2):
		pixels = get_pixel_array()
		wav_encode(pixels)

def contruct_image(array, width, height):
	#reassemble key image
	
	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	print(len(keypix))
	for i in range(len(keypix)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = keypix[i]
	return new_image

def printblue(text):
	print('\033[34m' + text + '\033[0m')

def printred(text):
	print('\033[31m' + text + '\033[0m')

def mean(numbers):
	return float(sum(numbers)) / max(len(numbers), 1)

def contruct_image(array, width, height):
	#reassemble key image
	
	new_image = Image.new('RGB', (width, height))
	data = new_image.load()

	for i in range(len(keypix)):
		xwidth = i / height
		xheight = i % height
		data[(xwidth, xheight)] = keypix[i]
	return new_image

def save_image(image):
	print("enter output file: (default sound.png)")
	fname = input()
	if fname=="":
		fname = "sound.png"
	image.save(fname)

def get_pixel_array():
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
			pix1.append(int(mean(cpixel)))
	return pix1

def wav_encode(pixels):
  
	sampleRate = 44100.0 # hertz
	duration = 1.0       # seconds
	frequency = 440.0    # hertz

	wavef = wave.open('sound.wav','w')
	wavef.setnchannels(1) # mono
	wavef.setsampwidth(2) 
	wavef.setframerate(sampleRate)

	for i in range(len(pixels)):
	   value = pixels[i]
	   data = struct.pack('<h', value)
	   wavef.writeframesraw(data)

	wavef.close()
	print("Converted and saved to sound.wav")

def get_wav_data():
	print("enter input file: (default sound.wav)")
	fname = input()
	if fname=="":
		fname = "sound.wav"
	wavef = wave.open(fname,'r')
	length = wavef.getnframes()  
	data = []
	i=0
	for i in range(length):
		bytedata = wavef.readframes(1)
		print(bytedata)
		stringdata = re.sub(r'b?n?\'','', re.sub(r'\\x', '', str(bytedata)))
		print(stringdata)
		data.append(int(stringdata, 16))

	print("done")
	return data

try:
	menu()
except KeyboardInterrupt as e:
	printred("quitting")
