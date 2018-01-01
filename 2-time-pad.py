from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import numpy

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

keypix = []

#xor data to get key
for i in range(0, len(pix1)):
	tuple1 = pix1[i]
	tuple2 = pix2[i]
	x = ()
	for i2 in range(0, len(tuple1)):
		xval = tuple1[i2] ^ tuple2[i2]
		x = x + (xval,)
	keypix.append(x)


#reassemble key image
width, height = image1.size

new_image = Image.new('RGB', (width, height))
data = new_image.load()

print len(keypix)
for i in range(len(keypix)):
	xwidth = i / height
	xheight = i % height
	data[(xwidth, xheight)] = keypix[i]

print "enter output file: (default key.bmp)"
fname3 = raw_input()
if fname3=="":
	fname3 = "key.bmp"
new_image.save(fname3, 'bmp')