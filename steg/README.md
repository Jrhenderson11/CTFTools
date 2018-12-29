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

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/Lucy-small.png "Original")

plane 0 (MSB):

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/plane0.bmp "MSB plane")

plane 1 (2nd bit):

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/plane1.bmp "2nd bit plane")
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

### qr-fixer
**`python3 qr-fixer.py`**

During the inter-ACE and volga CTFs there were a couple of challenges involving QR codes which didn't scan, so after spending hours manually editing them in an image editor I decided to make a tool that automated this stuff. There's a section about it below.

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
## QR Fixer:

Qr fixer is a tool made to fix difficult to scan QR-codes found in CTFs

Running it will make a menu that looks like

                                                   Images:
                 .::::::::    :::::::::            ╭──────────────────╮
                :+:    :+:   :+:    :+:            | imageX.png       |
               +:+    +:+   +:+    +:+             | imageX.png       |
              +#+    +:+   +#++:++#:               | imageX.png       |
             +#+    +#+   +#+    +#+               | imageX.png       |
            #+#    #+#   #+#    #+#                | imageX.png       |
            ########### ###    ###                 | imageX.png       |
                                                   | imageX.png       |
                    -- Fixer --                    | imageX.png       |
                                                   | imageX.png       |
        [1] Basic QR reconstruction                | imageX.png       |
        [2] Convert to black and white             | imageX.png       |
        [3] Overlay grid                           | imageX.png       |
        [4] Analyse size                           | imageX.png       |
                                                   | imageX.png       |
                                                   ╰──────────────────╯

where the box on the right will be filled with names of images in your local directory (to help with remembering file names)

### Basic Reconstruction

This will assume the image you have given is a closely cropped QR code with some noisy/incorrect image data, it will clean it up into sharp blcak and white squares for a qr code, and overwrite the basic elements needed for a QR code to function (alignment squares and lines).
Remember to use the --qrsize option to correctly select the qr size to create.

### Convert to black and white

Takes an image and attempts to flatten it to black and white as a preprocessing stage.
Note: this isn't greyscale: it will literally convert the image to black and white.

### Overlay grid

Shows you a copy of the input image with a grid overlayed to show you how the program will analyse this as a QR code
Remember to use the --qrsize option to correctly select the qr size to show

### Analyse size

Give this mode a closely cropped image of a QR code and it will analyse which qr code size results in the best match.
Currently it decides by measuring which size gets the basic alignment information most correct.
It will helpfully run the overlay grid function on the image to show to the user so they can decide if that's the right size.

### Example:

Here's a quick rundown of how the tool can be useful

`demo4.png` is taken from a spectrogram of a music file from a CTF, it is low res, green and blurry

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/demo4.png "Original")

First we run the **Convert to black and white** function
*Note I have cropped the image at this stage using an image editor, the program didn't do this*

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/qr_new2.png "Converted")

Now the output is clearly much easier to read, but still with enough imperfections to stop it being scanned

Next we can run the **Analyse size** function to get the size of qr code used

**Important: At this stage the image needs to be closely cropped to only include the QR code, otherwise stages from now on won't work**

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/analysis.png "Terminal")

*The dictionary shown in the command line output before the final descision shows how the algorithm works: it is a dictionary between qr size and how many squares in the basic patterns match, the higher the better. If you think it has decided incorrectly you could look for unususally high values to find the correct one*

And here is a grid size of 21 overlaid on the image:

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/qr_new2_analysed.png "Analysed")

We can clearly see this is the right size for this code

Armed with this information we can finally fully fix the image using the **Basic QR reconstruction** feature.
Since we know the size is 21 we run the program with

	./qr-fixer.py --qrsize 21

Select 1 from the menu, input the filename and we get this:

![alt text](https://github.com/Jrhenderson11/CTFTools/blob/master/steg/qr_new3.png "Final")

You can see since the original image was not perfectly square the algorithm has filled a column of black on the right side of the code but otherwise this is definitely what we want

From an imperfect image of a qr code we have fixed it to a perfect one that can be decoded

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