import os
from Crypto.Util.number import *

with open("flag.txt", "r") as f:
    flag = f.read().strip()

p = getPrime(1024)
q = getPrime(1024)
n = p*q
phi=(p-1)*(q-1)
d = p
e = inverse(d, phi)
flag=bytes_to_long(flag.encode())

c=pow(flag, e, n)
print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')