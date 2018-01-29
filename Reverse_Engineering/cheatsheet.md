# Reverse engineering Notes


gcc -z execstack -no-pie -fno-stack-protection

objdump ./a.out -d : dissasemble


##	gdb

break <\funcname>   : _install breakpoint in function call_

break <\*address>   : install breakpoint at specific address in instructions

run                : run program until breakpoint

run < args		   : simulate running with arguments

step / stepi       : step by 1 instruction

conti			   : proceed to next breakpoint

disas              : display dissasembled assembly code

x/256xb $rsp 	   : display stack

-------------------------------------------------------

##	Stack

RBP-RSP            : defines frame 
leave			   : collapse stack and exit

-------------------------------------------------------
## Python stuff

python -c "some code": execute from command line

DEMO CODE:
```python
	import sys
	sys.stdout.write(b"\x41"*128
	+b"\xP\xA\xY\xL\xO\xA\xD"[::-1]); # slice notation 
```
b: write as bytes
[::-1]: reverses end payload due to endianness

python print cannot hanlde null bytes; stdout.write can

Save payload to file and view:

	python attack.py > bin; xxd bin

Ropper is a tool for finding gadgets in executables
ropper --file a.out --search "pop"
looks for instructions
