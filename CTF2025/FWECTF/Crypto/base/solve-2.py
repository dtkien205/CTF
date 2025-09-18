#!/usr/bin/env python3
# -*- coding: utf-8 -*-

PAD = "🚀"

# đọc đúng file emoji.txt gốc
with open("emoji.txt", "r", encoding="utf-8") as f:
    emoji = list(f.read().strip())

reverse_table = {ch: i for i, ch in enumerate(emoji)}

def decode(s: str) -> bytes:
    s = s.rstrip(PAD)  # bỏ pad 🚀
    bits = ''.join(f"{reverse_table[ch]:010b}" for ch in s)
    out = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        out.append(int(byte, 2))
    return bytes(out)

if __name__ == "__main__":
    enc = "🪛🔰🛏🍈📛🤵🔈🚁📷🦨🥩💇💼🥇🧷🥳🎆🚇🔅👶📷🚇🤧🗣💐🥵🌚🦽🏖🧇🪥🦿🏋🛜🙆🧀🏋🔭🥬🍲🔫🚀🚀🚀"
    # enc tròn file output.bin

    dec = decode(enc)

    # Thử in ra chuỗi UTF-8
    try:
        print("Decoded text:", dec.decode("utf-8"))
    except:
        print("Decoded bytes (hex):", dec.hex())
