from __future__ import print_function
from Cryptodome.PublicKey import RSA

new_key = RSA.generate(4096)

public_key = new_key.publickey().exportKey("PEM")
private_key  = new_key.export_key("PEM")

public_key_file = open("public.pem","wb")
public_key_file.write(public_key)
public_key_file.close()

private_key_file = open("private.pem","wb")
private_key_file.write(private_key)
private_key_file.close()

print(public_key.decode())
print("\n" + private_key.decode())