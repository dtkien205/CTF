flag = "xakgK\\Ns9=8:9l1?im8i<89?00>88k09=nj9kimnu\00\00"

decode = ''.join(chr(ord(c) ^ 8) for c in flag)
print(decode)


# encrypted = "xakgK\\Ns>n;jl90;9:mjn9m<0n9::0::881<00?>u\00\00"

# decrypted = ''.join([chr(ord(c) ^ 8) for c in encrypted])
# print(decrypted)


