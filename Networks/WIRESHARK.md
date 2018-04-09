# WIRESHARK STUFF


use maginifying glass to search for string or regex


##Useful filters:

NOT, OR, AND

	! || &&

filter by source / destination address

	ip.src==<IP>
	ip.dst==<IP>

filter by port *for udp or other protocol replace tcp with protocol name*

	tcp.port==PORTNUM
	tcp.srcport==PORTNUM
	tcp.dstport==PORTNUM

find http form data (usernames, passwords etc.)

	http.request==POST

filter out annoing / spammy protocols

	!dns && !arp && !

find 
## Analysis:

Wireshark has a few nice tools for getting an overview of the data, expecially with large captures, these can be found in the **Analysis** or **Statistics** menus.

It is useful at first to get a quick overview of the activities in the capture, is it mainly web browsing? is it encrypted with https? are they downloading files?
A good way to do this is **Statistics > Protocol Heirarchy** which will show a breakdown of what protocols are used and how much of the capture they make up. This only applies to the current filter,so if you're already only looking at http packets it will tell you there are only http packets. This is useful because it means that you can apply a spam reducing filter to get a better picture of the actual user activity

**Statisitics > Endpoints** gives a nice 
breakdown of all the machines involved int he capture, and can be a quick way of e.g seeing all the websites somebody visited (tick name resolution to see the domain names and make sure name resolution is on in the default packet view first)

## SSL and HTTPS:

Https is encrypted http, using TLS or SSL encryption. To decrypt encrypted communications you will need the SSL keys used to initialise the encryption.

https://wiki.wireshark.org/SSL

You can look in the capture for the plaintext key if someone has left it there, or somehow obtain another key file, it will be an asymmetric key in the style 
	
```
-------- BEGIN PRIVATE KEY --------
Random Base64 string
--------- END PRIVATE KEY --------
```

Make sure you have this in a file, doesn't matter what it's called

The easiest way to do this is right click on one of the encrypted packets (with SSL or TLS protocol) and select **protocol preferences** then either **Open Secure Sockets Layer preferences** to go to the menu where you can add keys and stuff, or directly click on **import RSA keys** to go straight to the interface.

select the **+** symbol to add a new key and fill in the fields as follows:
 - IP Address: 	the server IP
 - Port: 		the server port (probably 443)
 - Protocol: 	if you are decrypting https use http, otherwise try raw
 - Key File: 	the path to the file in which you saved the RSA key

You can also get to the SSL preferences menu like this:
go to wireshark **edit > preferences**, go to the **Protocols** submenu, scroll down the list to find **SSL** (hint: it's a long way down) and change the settings there.

## Merging files:

https://www.wireshark.org/docs/wsug_html_chunked/AppToolsmergecap.html

## Tool for converting hex to packet data:

https://www.gasmi.net/hpd/