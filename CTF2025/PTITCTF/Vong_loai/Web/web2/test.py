import json, base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

jwk = {
    "kty": "RSA",
    "alg": "RS256",
    "kid": "PTIT-CTF",
    "use": "sig",
    "n": "zf1c1FAyg0btbcnxfuQzTQMqpi7RaZ78KQYLT69DgM9lJ6AfkhqUpuLCwK4NL0emQgbj2CkVGvTQKyejhCqQE9RagMgFFl2o2kpJpEIfab08XB0tqJn-q770xUgUQPA1h9PlD2SnHmorVNwOKcKGSj862CryvS2b7Xf3BkKCt_75AlbUGGTS9RumrZIeQYfyVfTERuRtaus3Et2KWwRA_DCAg19k3YGcs2dKqzUZwL-OqogA5PobjrEzlmVuWpe5bIuzW1mP_lkdaEWwJxF2yAZBF_aQlAVYSLMAW3Z2stU3cwLtCb2M2sJOMmn6cG6cBEr3Yw2lgiiQNGne3WJSOw",
    "e": "AQAB"
}

def b64url_to_int(val):
    data = base64.urlsafe_b64decode(val + '=' * (-len(val) % 4))
    return int.from_bytes(data, 'big')

n = b64url_to_int(jwk['n'])
e = b64url_to_int(jwk['e'])

public_key = rsa.RSAPublicNumbers(e, n).public_key()

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(pem.decode())
