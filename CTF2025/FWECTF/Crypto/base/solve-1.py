#!/usr/bin/env python3
# -*- coding: utf-8 -*-

PAD = "🚀"

# ⚠️ Bạn cần thay file emoji.txt bằng đúng bản gốc khi encode
with open("emoji.txt", "r", encoding="utf-8") as f:
    emoji = list(f.read().strip())

reverse_table = {ch: i for i, ch in enumerate(emoji)}

def decode(s: str) -> bytes:
    s = s.rstrip(PAD)  # bỏ padding 🚀
    bits = ''.join(f"{reverse_table[ch]:010b}" for ch in s)
    out = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        out.append(int(byte, 2))
    return bytes(out)

if __name__ == "__main__":
    enc = "🪛🔱🛜🫗🚞👞🍁🎩🚎🐒🌬🧨🖱🥚🫁🧶🪛🔱👀🔧🚞👛😄🎩🚊🌡🌬🧮🤮🥚🫐🛞🪛🔱👽🔧🚞🐻🔳🎩😥🪨🌬🩰🖖🥚🫐🪐🪛🔱👿🫗🚞🏵📚🎩🚊🎄🌬🧯🕺🥚🫁📑🪛🔰🐀🫗🚞💿🔳🎩🚲🚟🌬🧲🚯🥚🫁🚰🪛🔱💀🔧🚞🏓🛼🎩🚿🪻🌬🧪🙊🥚🫐🧢🪛🔱🛟🔧🚞🚋🫳🎩😆🏉🌬🧶🚓🥚🫅💛🪛🔱🔌🐃🚞🐋🥍🎩😱🤮🌬🩰🛳🥚🫀📍🪛🔰🐽🫗🚞💿🍁🎩🚊🌋🌬🧵🔷🚀🚀🚀"

    dec = decode(enc)

    # In ra vài dạng để dễ kiểm tra
    print("Decoded bytes (hex preview):", dec[:64].hex(), "...")

    # Lưu ra file nhị phân
    with open("output.bin", "wb") as f:
        f.write(dec)
    print("Đã lưu vào output.bin")
