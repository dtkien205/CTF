import json

data = {}

# 256 keys ra 0: "0", "00", ..., "0"*256
for i in range(1, 257):
    data["0" * i] = 0

# 256 keys ra 1: "1", "01", ..., "0"*255 + "1"
for i in range(0, 256):
    data["0" * i + "1"] = 1

# Nhét "Holactf" vào value của key "0"
data["0"] = "Holactf"

payload = {"data": data}

# Xuất ra dạng JSON đẹp
print(json.dumps(payload, indent=2))
