#     Steganography notes

----------------------------------------------------------------------------
## Steganography Techniques

Steganography is the art of hiding stuff blah blah blah, ancient romans / greeks blah blah blah

As opposed to encryption or hashing the aim is more to hide the fact the additional information is there at all as a method of protecting it. It is commonly done by hiding text or another image in another legitimate file, thereby disguising it.

**Bit plane slicing:**

Images are made up of an array of pixels. Ignoring the differences between different encodings / file formats etc. what a pixel contains is a number representing the colour or shade. This number can be represented as binary e.g a white pixel value *255* is *11111111*
Because of the way binary (and any number base) works the digits / bits on the left contain a larger value than those on the right, the leftmost is the Most Significant Bit (MSB) and the rightmost is the LSB.
This means that most of the value is encoded in the left bits of the number. Changing the MSB will roughly double or halve the value, whereas changing the LSB will add or subtract one.
In terms of colour this means changing the MSB will result in a dramatic change of colour whereas changing the LSB will be unoticable (for a standard 8-bit colour image).
An image composed only of the bits of one position e.g all the MSBs is called a **bit plane**. here are the 2 upper bit planes of the image Lucy-small.png:

original:

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/Steg/Lucy-small.png "Original")

plane 0 (MSB):

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/Steg/plane0.bmp "MSB plane")

plane 1 (2nd bit):

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/Steg/plane1.bmp "2nd bit plane")
You can view all the other planes as well in this folder.

Because of this you can change the LSB (and actually quite a few of the last bits of the number) of the pixels with barely any effect on the visible image.
This means a binary (2-bit colour, black and white) image could be created and exchanged for one of the planes of another image. If the plane replaced is an unsignificant one this will not be visible in the image and only visible when the image is split into its constituent planes

In theory this allows any alteration of an image to be found by analysing the expected noise levels in bit planes, read more about this technique and bit plane steg here: 
	
https://incoherency.co.uk/blog/stories/image-steganography.html

----------------------------------------------------------------------------
## My Tools:

### stegger
**`python stegger.py`**

Does bloody loads of stuff.
Basically a container for loads of image manipulation / steganography techniques. A bit WIP currently, but has a nice menu

### waver
**`python3 waver.py`**

waver is a tool made for the volga CTF 2018 to decode an image into a wav file, I'm working on implemnting the reverse process as well, take a look at *sound.png* and *sound.wav* to see the input / output

----------------------------------------------------------------------------
## Other Tools:

### strings
**`strings <file>`**

displays plaintext strings found in a file

### exiftool
**`exiftool <file>`**

extracts exif metadata from image files  

### playitslowly
**`playitslowly <file>`**

found this when I needed to manipulate an audio file to find a hidden message
it can reverse, slow down and change the frequencies of an audio file

https://github.com/jwagner/playitslowly

### audacity
**`audacity <file>`**

Another useful tool for manipulating and playing audio files

### sonic-visualiser
**`sonic-visualiser <file>`**

Can find images hidden in the notes of a music file
Use `Layer>Add Spectrogram` to see the information 

### foremost
**`foremost <file>`**

A file carving tool, based on **scalpel** but better. Analyses a file for files using file carving, places its output in a folder called **output**
Annoyingly if you run it twice it complains unless you delete the output folder with *rm -rf output*
After installing uncomment lines in `/etc/foremost.conf` to be able to carve differnet file types


----------------------------------------------------------------------------

## Useful Links:

website with file headers:
https://www.garykessler.net/library/file_sigs.html

----------------------------------------------------------------------------

## Other Stuff:

While doing a steganography challenge in a CTF there was a picture of a woman, called Lena.tif. 
Whilst researching different steganography methods I came accross a website that did online steganography, and in the sample images they had I found the same picture of the woman, also called Lena. I got kind of excited and thought I had found the exact tool they used to encode the image. But I hadn't.
I kept coming across the image while looking up steganography stuff and realised it was just a common example image used for steganography.

When writing the *Bit Plane slicing* section of this file I wanted to include some demo images, so used the example Lena.tif file and 2 of the bit planes I had created when analysing the file for the CTF. I still didn't know why this was the image commonly used as a demo but after spending ~17 hours staring at subtley different blurry versions of this image with QR codes in I felt that I might as well use this as my example. I put this text in this *Other Stuff* section: 

	The image of Lena is commonly used as an example for steganography, I don't know why, maybe she was a pioneer of some of the methods?

Later I realised the images were way too big, so I went to resize them and when I did I also decided to look up who Lena was. After looking through the wikipedia page of famous people called Lena (there are a lot) I found this:

https://en.wikipedia.org/wiki/Lenna

So the picture is a standard for all image processing, not just steganography but sadly it is from playboy, a deeply sexist publication. As also pointed out by the wikipedia page, using an image like that as a standard example is contributing to the sexism and male-dominance in science and computer science and as quoted in the wikipedia page has a "detrimental impact on aspiring female students in computer science".

The page http://www.ee.cityu.edu.hk/~lmpo/lenna/Lenna97.html gives more detail and says she was invited to a conference on digital image processing as a special guest which is quite nice I suppose. Maybe even more interestingly the site says 
	
	Currently, Lenna lives near Stockholm and works for a government agency supervising handicapped employees archiving data using, appropriately, computers and scanners

which is nice.

But due to its sexist connotations I'm not going to use it as an example image, I'm going to use a picture of my cat instead.