import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

e = 0x010001
n = 0xC6237B64ABB97CFBE590A65C5545143CDFCB86C2C7ED39E66925F09D63D07185
q = 295113122891357775740359577253851897513
p = 303682311439016350992650842927032652157
phi = (p -1)*(q-1)

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)
	
def modinv(a, m):
	gcd, x, y = egcd(a, m)
	if gcd != 1:
	    return None  # modular inverse does not exist
	else:
	    return x % m
 
d = modinv(e,phi)


dp = modinv(e,(p-1))
dq = modinv(e,(q-1))
qi = modinv(q,p)

def pempriv(n, e, d, p, q, dP, dQ, qInv):
	template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
	seq = pyasn1.type.univ.Sequence()
	for x in [0, n, e, d, p, q, dP, dQ, qInv]:
	    seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
	der = pyasn1.codec.der.encoder.encode(seq)
	return template.format(base64.encodestring(der).decode('ascii'))
 
key = pempriv(n,e,d,p,q,dp,dq,qi)
print key