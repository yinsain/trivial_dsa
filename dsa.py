#!/usr/bin/env python3
import prime
import random
import hashlib

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

def keyGeneration():
    q = prime.generate_prime_number()
    g = prime.prim_root(q)
    a = random.randrange(1, q)
    y1 = pow(g, a, q)
    y2 = pow(y1, a, q)
    return (q, a, g, y1, y2)

def signatureGeneration(msg, g, a, q, y1, y2):
    r = random.randrange(1, q)
    A = pow(g, r, q)
    B = pow(y1, r, q)
    c = hashlib.sha1((str(A) + str(B) + str(msg.strip())).encode()).hexdigest()
    c = int(c, 16)
    s = ((a * c) + r) % (q - 1)
    return (r, c, s)

def signatureVerification(s, q, g, y1, y2, c, msg):
    s = int(s);q = int(q);g = int(g);y1 = int(y1);y2 = int(y2);c = int(c)
    A = (pow(g, s, q) *  pow(modinv(y1, q), c, q)) % q
    B = (pow(y1, s, q) * pow(modinv(y2, q), c, q)) % q
    cnew = hashlib.sha1((str(A) + str(B) + str(msg.strip())).encode()).hexdigest()
    cnew = int(cnew, 16)
    if cnew == c:
        return (True, A, B, cnew)
    else:
        return (False, A, B, cnew)

# # # #
# q, key, g, y1, y2 = keyGeneration()
# r, c, s = signatureGeneration('yashdeep', g, key, q, y1, y2)
# print(signatureVerification(s, q, g, y1, y2, c, 'yashdeep'))
