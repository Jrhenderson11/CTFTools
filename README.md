# CTFTools
A collection of scripts / tools I've made for capture the flag style challenges / playing with security testing stuff


## Tools:

- Crawler.py: A simple web crawler that shows "flag" in the comments, robots file or cookies of a website and checks for the presence of word "flag"

- 2-time-pad.py: A tool I made in a CTF to xor 2 images encrypted with a 1 time pad to get the key

- capper.py: A tool used in a CTF to reconstruct a message hidden in pcap obfuscated with ARP poisoning
			 basically a demo of using python to interact with .pcap files and inspect packets

- crypter.py: A really simple demo of using the Crypto library to encrypt/decrypt 

- passwordpredicter.py: A bunch of useful functions for generating passwords (unfinished)


## Files:

 - numbers.txt: Ordered list of most common number combinations found after letters in passwords (based on rockyou)
 - patterns.txt: Ordered and counted list of passwords patterns: ie password123 is CCCCCCCCDDD (based on rockyou)

### Note:

I would like to have added the actual rockyou files, but uncompressed they exceed the file size limit, therefore I will provide the link to a site where you can download them: https://wiki.skullsecurity.org/Passwords


## TODO:

 - finish passwordpredicter
 - fuzzer
 - forensic thingy?
 - steg?
 - notes

