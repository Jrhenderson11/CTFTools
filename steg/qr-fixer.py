#!/usr/bin/python3
import os
import re
import sys
import math
import pyzbar
import numpy
import argparse
from os import listdir, walk
from os.path import isfile, join
from colorama import Fore, Style
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

RESET = Fore.RESET+ Style.NORMAL
BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
BRIGHT_RED = Fore.RED + Style.BRIGHT

class QR_Fixer():
	
	def __init__(self, qr_size=29, minimal=False):
		self.qr_size = qr_size
		self.minimal = minimal

	def attach_ls(self, text):
		files = []
		max_length = 0
		for f in listdir("./"):
			if isfile(join("./", f)) and (len(re.findall(r'(png|jpg|tif|bmp)', f)) > 0):
				files.append(f)
				if len(f) > max_length:
					max_length = len(f)

		width = max_length + 4
		lines = [line.replace("	", "    ") for line in text.split("\n")]
		offset = 51
		
		lines[0] = ("{:"+str(offset)+"}").format("") +BRIGHT_GREEN+" Images:"
		# Draw box
		lines[1] = "\033[34m" + lines[1][:offset] +BRIGHT_GREEN + str("╭") + "─" * (width-1) + "╮"
		for i in range(2, len(lines)-1):
			lines[i] = "\033[34m" + lines[i] + (" " * (offset - len(lines[i].replace(BRIGHT_RED, "").replace(RESET, "").replace("\033[34m", "").replace("\033[97m", "").replace("\033[1m", "").replace("\033[0m", "")))) +BRIGHT_GREEN+"| " + (("{:"+str(width-2)+"}").format(files[i])) + "|" + "\033[0m"
		lines[-1] = "\033[34m" + ("{:"+str(offset)+"}").format("") +BRIGHT_GREEN+"╰" + "─" * (width-1) + "╯" + "\033[0m"

		return "\n".join(lines)

	def print_intro(self, ):
		text = '''\033[34m
		         .::::::::    :::::::::  	  	
		        :+:    :+:   :+:    :+: 	
		       +:+    +:+   +:+    +:+  	
		      +#+    +:+   +#++:++#:    	
		     +#+    +#+   +#+    +#+    	
		    #+#    #+#   #+#    #+#     	
		    ########### ###    ###  	   	  \n
	\033[1m\033[97m	            -- Fixer --\033[0m'''
		return text

	def get_menu_text(self, ):
		return '''		\033[97m[1] Basic QR reconstruction
		\033[97m[2] Convert to black and white
		\033[97m[3] Overlay grid
		\033[97m[4] Analyse size\n
	'''

	def menu(self):
		try:
			text = ""
			if not self.minimal:
				os.system("clear")
				text = self.print_intro()+ "\n\n"
			text += self.get_menu_text()
			if not self.minimal:
				print(self.attach_ls(text))
			else:
				print(text)
			try:
				i = input()
				num = int(i)
			except ValueError as e:
				if (i=="q"):
					exit(0)
				num = -1
			while not (num>0 and num<5):
				text = ""
				if not self.minimal:
					os.system("clear")
					text = self.print_intro()
				text += "\n         	"+BRIGHT_RED+"  invalid input "+RESET+"		  \n"
				if not self.minimal:
					text+=self.get_menu_text()
				if not self.minimal:
					print(self.attach_ls(text))
				else:
					print(text)
				try:
					i = input()
					num = int(i)
				except ValueError as e:
					if (i=="q"):
						exit(0)
					num = -1

			if (num==1):
				self.basic_repair()
			if (num==2):
				self.flatten_image()
			if (num==3):
				self.overlay_grid()
			if (num==4):
				self.analyse_size()
		except KeyboardInterrupt as e:
			print(BRIGHT_RED + "quitting" + RESET)

	# ---- Main Functions ----
	
	def decode(self):
		default = "qr.png"
		fname = input("enter input file: (default " + default + ")\n")
		if fname=="":
			fname = default
		res = pyzbar.decode(Image.open(fname))
		print(res)
	
	def basic_repair(self):

		(pixels, width, height) = self.get_image_data("qr.png")
		print("width: {}".format(width))
		print("height: {}".format(height))

		blocks = numpy.zeros((self.qr_size, self.qr_size))

		block_width = (width / self.qr_size)
		block_height = (height / self.qr_size)

		for block_y in range(self.qr_size):
			for block_x in range(self.qr_size):

				black, white = 0,0
				
				for small_y in range(int(block_height)):
					for small_x in range(int(block_width)):

						x = (round(block_x*block_width) + small_x)
						y = (round(block_y*block_height) + small_y)

						total, continuous = 0,0
						
						avg = (pixels[x,y][0] + pixels[x,y][1] + pixels[x,y][2]) / 3	
						#TODO: adjust flattening to match max and min within a range
						pixel = 255 if avg > 127 else 0

						if (pixel == 0):
							black += 1
						else:
							white += 1

						# Right
						# if small_x != int(block_width):
						# 	total +=1
						# 	current = 255 if avg > 127 else 0
						# 	next = 255 if (pixels[x+1,y][0] + pixels[x+1,y][1] + pixels[x+1,y][2]) / 3 > 127 else 0
						# 	if current==next:
						# 		continuous+=1
						# # Down
						# if small_y != (block_height):
						# 	total +=1
						# 	current = 255 if avg > 127 else 0
						# 	next = 255 if (pixels[x,y+1][0] + pixels[x,y+1][1] + pixels[x,y+1][2]) / 3 > 127 else 0
						# 	if current==next:
						# 		continuous+=1

				m = 0
				#print("({},{}): {}-{} =   {}".format(block_x, block_y, black, white, black-white))
				print("{:6}".format("{}:{}".format(black, white)), end="")
				if black > white: #and continuous > total*0.9:
					blocks[block_x, block_y] = 1
				else:
					blocks[block_x, block_y] = 0
			print("")

		blocks = self.overwrite_fixed_patterns(blocks)

		qr_image = self.make_qr_image(blocks, width, height)
		qr_image.show()
		self.save_image(qr_image)

	def overwrite_fixed_patterns(self, qr_array):
		
		x=0
		y=0

		#vertical
		for y2 in range(self.qr_size-7, self.qr_size):
			qr_array[0, y2] = 1
			qr_array[6, y2] = 1

		for (x,y) in [(0,0), (self.qr_size-7,0), (0,self.qr_size-7)]:
			#corner boxes
			
			#white outline
			for x2 in range(-1, 8):
				for y2 in (-1, 8):	
					if ((x+x2) > 0 and (x+x2) < self.qr_size) and ((y+y2) > 0 and (y+y2) < self.qr_size):
						qr_array[x+x2, y+y2] = 0

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

		#dotted lines
		for x in range(7, self.qr_size-7):
			if x%2==0:
				qr_array[x, 6]=1
				qr_array[6, x]=1
			else:
				qr_array[x, 6]=0
				qr_array[6, x]=0

		#small alignment square
		for x in range(self.qr_size-9, self.qr_size-4):
			qr_array[x,self.qr_size-9] = 1
			qr_array[x,self.qr_size-5] = 1
			qr_array[self.qr_size-9,x] = 1
			qr_array[self.qr_size-5,x] = 1
		qr_array[self.qr_size-7,self.qr_size-7] = 1

		return qr_array

	def flatten_image(self):
		(pixels, width, height) = self.get_image_data("demo.png")
		newpixels = numpy.zeros((width, height))

		#get max and min val
		midsum = 0
		for x in range(width):
			for y in range(height):
				avg = (pixels[x,y][0] + pixels[x,y][1] + pixels[x,y][2]) / 3	
				midsum+=avg

		middle = midsum / (width*height) 


		for x in range(width):
			for y in range(height):
				avg = (pixels[x,y][0] + pixels[x,y][1] + pixels[x,y][2]) / 3
				

				#TODO: adjust flattening to match max and min within a range
				newval = 255 if avg > middle else 0
				
				newpixels[x,y] = newval

		image = self.construct_image_2d(newpixels, width, height)
		image.show()
		self.save_image(image)

	def overlay_grid(self):
		
		(pixels, width, height) = self.get_image_data("demo2.jpg")
		block_width = (width / self.qr_size)
		block_height = (height / self.qr_size)

		for x in range(width):
			for y in range(height):
				if int(x%block_width)==0 or int(y%block_height) == 0:
					pixels[x,y] = (255,0,0)

		image = self.construct_image_2d_tuples(pixels, width, height)
		image.show()

	def analyse_size(self):
		# Attempt to work out the size of given qr code
		# Find size which basic pattern fits best, then rank by entropy

		(pixels, width, height) = self.get_image_data("qr_new0.png")
		
		matches = {}
		print("Calculating...")
		# Loop through possible qr code sizes
		for qr_size in range(21, 178, 4):
			blocks = numpy.zeros((qr_size, qr_size))
			
			total_entropy = 0.0
			
			for block_y in range(qr_size):
				for block_x in range(qr_size):

					colours = [0, 0]
					for small_y in range(int(height/qr_size)):
						for small_x in range(int(height/qr_size)):
							
							x = (int(block_x*width/qr_size) + small_x)
							y = (int(block_y*height/qr_size) + small_y)

							# Flatten
							pixel = 255 * math.floor(pixels[x,y][0]/128)

							if (pixel == 0):
								colours[1] = colours[1] + 1					
							else:
								colours[0] = colours[0] + 1
					# Crude but it doesn't matter
					if colours[1]>colours[0]:
						blocks[block_x, block_y] = 1
					else:
						blocks[block_x, block_y] = 0
			
			matches[qr_size] = self.match_fixed_patterns(blocks, qr_size)		
		print(matches)
		ranked = sorted(matches.keys(), key=lambda x: matches[x], reverse=True)
		best = ranked[0]
		print(BRIGHT_GREEN + "Best matched size is " + str(best) + RESET)
		block_width = (width / best)
		block_height = (height / best)

		for x in range(width):
			for y in range(height):
				if int(x%block_width)==0 or int(y%block_height) == 0:
					pixels[x,y] = (255,0,0)

		image = self.construct_image_2d_tuples(pixels, width, height)
		image.show()
	
	def match_fixed_patterns(self, qr_array, qr_size):
		
		x, y = 0, 0
		total = 0

		#vertical
		for y2 in range(qr_size-7, qr_size):
			total+=1 if qr_array[0, y2] == 1 else 0
			total+=1 if qr_array[6, y2] == 1 else 0

		for (x,y) in [(0,0), (qr_size-7,0), (0,qr_size-7)]:
			#corner boxes
			
			#white outline
			for x2 in range(-1, 8):
				for y2 in (-1, 8):	
					if ((x+x2) > 0 and (x+x2) < qr_size) and ((y+y2) > 0 and (y+y2) < qr_size):
						total+=1 if qr_array[x+x2, y+y2] == 0 else 0

			#horizontal lines
			for x2 in range(7):
				total+=1 if qr_array[x+x2, y] == 1 else 0
				total+=1 if qr_array[x+x2, y+6] == 1 else 0
			
			#vertical
			for y2 in range(7):
				total+=1 if qr_array[x, y2] == 1 else 0
				total+=1 if qr_array[x+6, y2] == 1 else 0

			#centre
			for y2 in range(3):
				for x2 in range(3):
					total+=1 if qr_array[x+2+x2,y+2+y2] == 1 else 0
		temp = 0.0
		#dotted lines: because these depend on size they need to be normalised
		for x in range(7, qr_size-7):
			if x%2==0:
				temp+=1 if qr_array[x, 6]==1 else 0
				temp+=1 if qr_array[6, x]==1 else 0
			else:
				temp+=1 if qr_array[x, 6]==0 else 0
				temp+=1 if qr_array[6, x]==0 else 0
		temp = int(temp/qr_size-14)
		total += temp
		#small alignment square
		for x in range(qr_size-9, qr_size-4):
			total+=1 if qr_array[x,qr_size-9] == 1 else 0
			total+=1 if qr_array[x,qr_size-5] == 1 else 0
			total+=1 if qr_array[qr_size-9,x] == 1 else 0
			total+=1 if qr_array[qr_size-5,x] == 1 else 0
		total+=1 if qr_array[qr_size-7,qr_size-7] == 1 else 0

		return total
	
	#
	# ---- Image IO ----

	def get_image_data(self, default):
		
		fname = input("enter first file: (default " + default + ")\n")
		if fname=="":
			fname = default

		exists = True

		try:
			image = Image.open(fname, 'r')
		except FileNotFoundError as e:
			exists = False

		while (exists==False):
			exists = True
			print(BRIGHT_RED + "File " + fname + " not found" + RESET)
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

	def make_qr_image(self, qr_array, width, height):

		qr_image = Image.new('RGB', (width, height))
		pixels = qr_image.load()

		qr_size = len(qr_array[0])
		block_size = width / qr_size

		for block_y in range(qr_size):
			for block_x in range(qr_size):
				for small_y in range(int(height/qr_size)+1):
					for small_x in range(int(height/qr_size)+1):
						try:
							x = ((block_x*height/qr_size) + small_x)
							y = ((block_y*height/qr_size) + small_y)
							block = qr_array[block_x, block_y]
							pixels[(x, y)] = (255-(255 * int(block)), 255-(255 * int(block)), 255-(255 * int(block))) 
						except:
							pass

		return qr_image

	def construct_image(self, array, width, height):
		#reassemble key image

		new_image = Image.new('RGB', (width, height))
		data = new_image.load()

		print(len(array))
		for i in range(len(array)):
			xwidth = i / height
			xheight = i % height
			data[(xwidth, xheight)] = array[i]
		return new_image

	def construct_image_2d(self, array, width, height):

		new_image = Image.new('RGB', (width, height))
		data = new_image.load()

		#print(len(array))
		for x in range(width):
			for y in range(height):
				val = array[x, y]
				data[x, y] = int(val), int(val),int(val) 
		return new_image

	def construct_image_2d_tuples(self, array, width, height):

		new_image = Image.new('RGB', (width, height))
		data = new_image.load()

		#print(len(array))
		for x in range(width):
			for y in range(height):
				val = array[x, y]
				data[x, y] = val 
		return new_image

	def save_image(self, image):
		num = self.get_num_files("qr_new")
		print("enter output file: (default qr_new"+str(num)+".png)")
		fname = input()
		if fname=="":
			fname = "qr_new"+str(num)+".png"
		image.save(fname)

	def get_num_files(self, base):
		onlyfiles = "".join([(" " + f) for f in listdir("./") if isfile(join("./", f))])
		return len(re.findall((base + "\d+\."), onlyfiles))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Fixes up low quality QR codes")
	parser.add_argument("--minimal", help="Don't clear screen or show ascii art")
	parser.add_argument("--qrsize", type=int,help="Size of QR code to use (default 29)", default=29) # 25, 29 33

	args = parser.parse_args()

	fixer = QR_Fixer(qr_size=args.qrsize, minimal=args.minimal)
	fixer.menu()

# TODO:

# brute force based on certainty
# input log
# ls command
# add ability to turn image menu off
# highlight differences