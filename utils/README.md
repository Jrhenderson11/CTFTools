# Flagger

A tool to search input for CTF flag like strings


## Modes

Flagger has 2 basic functions from the command line:
 - Taking input from a file and sorting it by flagness
 - Taking a stream of input and highlighting flags in green

If you run flagger as `./flagger.py <file>` flagger will execute the sorting mode on this file and output to the command line

If you pass flagger input to stdin ie `cat file | ./flagger.py` flagger will execute the highlighting mode

You will always want to pass flagger a string such as CTF so it can recognise flags in the format CTF{th1s_is_4_fl4g!}, otherwise it will default to flag{th1s_is_4_fl4g!}

## Command line options  

usage: flagger.py [-h] [--intro INTRO] [--minimal] [--reverse] [filename]

CTF flag detector

positional arguments:
  filename       file path to use as input

optional arguments:
  -h, --help     show this help message and exit
  --intro INTRO  string to replace flag in flag\{\}
  --minimal      Don't display input that isn't flag like
  --reverse      display result of sort upside down (best amtches at bottom)

### Example application

You have a file to investigate, so you run strings on it, but the strings are huge and you want quickly to see any flag-like strings in it

	strings interesting.png > strings_file.txt && ./flagger.py --intro <INTRO> strings_file.txt | ./flagger.py --intro <INTRO> --minimal 

This command will make a file with a long list of strings, most of whcih will be nonsense, then sort them based on which are likely to be flags and then highlighting the best, discarding anything that can't be a flag

the output will be a nice list of possible flags with all the useless data discarded

### Note:

This tool will interpret flags as anything between braces with words separated by underscores, it will not highlight regular english text