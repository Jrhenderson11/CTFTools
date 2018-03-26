#     Steganography notes

------------------------
##  Tools:

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


## Useful Links:

website with file headers:
https://www.garykessler.net/library/file_sigs.html