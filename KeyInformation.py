from Crypto.PublicKey import RSA

private_url = "BTL/private_key.pem"
public_url = "BTL/public_key.pem"
with open(private_url, "rb") as f:
    private_key = RSA.import_key(f.read())
with open(public_url, "rb") as f:
    public_key = RSA.import_key(f.read())


n = private_key.n
e = private_key.e
d = private_key.d
p = private_key.p
q = private_key.q
dP = private_key.d % (p - 1)
dQ = private_key.d % (q - 1)
qInv = private_key.u

# Extract components from the public key
n_pub = public_key.n
e_pub = public_key.e

# Print the components
print(f"Private Key Components:")
print(f"n  (modulus)       : {n}")
print(f"e  (public exponent): {e}")
print(f"d  (private exponent): {d}")
print(f"p  (prime 1)        : {p}")
print(f"q  (prime 2)        : {q}")
print(f"qInv (q^-1 mod p)   : {qInv}")

print(f"\nPublic Key Components:")
print(f"n  (modulus)       : {n_pub}")
print(f"e  (public exponent): {e_pub}")