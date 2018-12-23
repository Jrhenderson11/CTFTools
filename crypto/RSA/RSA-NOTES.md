# RSA NOTES

Some notes compiled from the C2C qualifying CTF on RSA keys, the challenge was to brute force a weak (256 bit) RSA key

Some people are interested in the fancy crypto maths stuff. I'm not really. If you are there are *lots* of places you can find that information, here are some I guess:

https://en.wikipedia.org/wiki/RSA_(cryptosystem)

https://hackernoon.com/how-does-rsa-work-f44918df914b

and here's a practical guide (the one I used to do the challenge so it's pretty much the same as method 2 in the demo)

http://b3ck.blogspot.co.uk/2011/06/how-to-break-rsa-explicitly-with.html

**openssl rsautl** is the best command line program for RSA encryption techniques

------------------------------
## Generating keys

Key generation is done with **openssl genpkey**

here's the code to generate a useful RSA private key

	openssl genpkey -algorithm RSA -out key.priv -pkeyopt rsa_keygen_bits:2048

we can generate the corresponding public key

	openssl rsa -pubout -in key.priv -out key.pub

now we have a valid public and private key pair to use for asymmetric encryption

------------------------------
## Encryption

The idea of asymmetric encryption is that the plaintext is encrypted with one of the keys and decrypted with the other, you encrypt with a public key and decrypt with the private. 

This command encrypts the file test.txt into test.enc with the public key key.pub

	openssl rsautl -encrypt -pubin -inkey key.pub -in test.txt -out test.enc

*warning: dunno why but if you encrypt with the private key the payload also decrypts with the private key, maybe openssl automatically generates the public key and decrypts it, but anyway, don't rely on people needing the public key if you encrypt with the private*

## Decryption

A payload encrypted with the public key needs to be decrypted with the private key

	openssl rsautl -decrypt -inkey key.priv -in test.enc -out test.enc

*Another warning: you will need to watch out for padding options, if you know you have the right key for decryption try altering the padding option, e.g adding **-raw** at the end*

## Key brute forcing demo:

One challenge in the C2C qualifying CTF was to decrypt a file given a weak public key it had been encrypted with. The idea of RSA encryption is that the private key cannot be guessed with the public, but with a key this small the number of possibilities is reduced to the point at which it's feasible

---------------------------------
### Setup:

first make a payload, a weak key pair and encrypt the key

	echo "secret_stuff" > test.txt

and make the keypair

	openssl genpkey -algorithm RSA -out weak.priv -pkeyopt rsa_keygen_bits:256

	openssl rsa -pubout -in weak.priv -out weak.pub

and encrypt:

	openssl rsautl -encrypt -pubin -inkey weak.pub -in test.txt -out test.enc

now if we didn't have the private key this should be impossible to decrypt

if you want to be sure

	rm weak.priv

So now we can atack using only the public key


#### Method 1:

There's a tool that does it for you! 
https://github.com/Ganapati/RsaCtfTool
sometimes

#### Method 2:
Step 1 is to analyse the public key

	openssl rsa -in key.pub -pubin -text -modulus

This will print something like this, we are interested in the exponent and the *Modulus=HEXSTRING* part

	Public-Key: (256 bit)
	Modulus:
	    00:c6:23:7b:64:ab:b9:7c:fb:e5:90:a6:5c:55:45:
	    14:3c:df:cb:86:c2:c7:ed:39:e6:69:25:f0:9d:63:
	    d0:71:85
	Exponent: 65537 (0x10001)
	Modulus=C6237B64ABB97CFBE590A65C5545143CDFCB86C2C7ED39E66925F09D63D07185
	writing RSA key
	-----BEGIN PUBLIC KEY-----
	MDwwDQYJKoZIhvcNAQEBBQADKwAwKAIhAMYje2SruXz75ZCmXFVFFDzfy4bCx+05
	5mkl8J1j0HGFAgMBAAE=
	-----END PUBLIC KEY-----

The first thing to do with the modulus is to translate it to a decimal number, a good way to do this could be int(HEXSTRING, 16) in python or use the amazing https://www.asciitohex.com/ which gives us a bloody long number

	89620635295634017606461759838019258794237250792881444486050811341563342385541

This number needs to be factorised into 2 primes p and q, we can use the program **msieve** to do that, it can be downloaded from here: https://sourceforge.net/projects/msieve/, extract it somewhere and then I think you just run `make` and it will give you your executable.
To factorise the modulus run this command with the decimal modulus

	sudo msieve-1.53/msieve -v NUMBER

after a bit it will print a bunch of irrelevant stuff and also some useful stuff:

	p39 factor: 295113122891357775740359577253851897513
	p39 factor: 303682311439016350992650842927032652157

these are our p and q values, now we need to recombine them with the modulus and exponent to get our private key.
To do this use the file here **rsaer.py**
which I basically nicked from https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/
Replace the values of p and q with the p39 factors, replace the exponent with the one from step 1, and the modulus with the one from step 1, run it and it will spit out a private key, you can pipe this into a file e.g

	python rsaer.py > broken.priv

now try to use this new key to decrypt it (maybe attaching the -raw option)

	openssl rsautl -decrypt -inkey broken.priv -in test.enc -raw

and we get out some bollocks and our original plaintext!

	Ȩ]l`�i�Y%��
	Asecret_stuff

yay!