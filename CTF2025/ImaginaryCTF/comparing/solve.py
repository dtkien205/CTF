out_lines = [
"9548128459",
"491095",
"1014813",
"561097",
"10211614611201",
"5748108475",
"1171123",
"516484615",
"114959",
"649969946",
"1051160611501",
"991021",
"1231012101321",
"9912515",
"11411511",
"1151164611511"
]

def parse_even(s):
    # cấu trúc: val1 + val3 + i + reverse(val1+val3)
    half = (len(s) - len(s)//2)  # không chuẩn, xử lý đơn giản hơn:
    # ta tách ra phần đầu và phần cuối
    # ví dụ: 9548128459 -> val1=95, val3=48, i=12
    # reverse("9548") = "8459"
    # ta thử brute split
    for i in range(1, 4):
        for j in range(1, 4):
            val1 = int(s[:i])
            val3 = int(s[i:i+j])
            idx = len(s) - (i+j)
            k = s[i+j:idx]
            tail = s[idx:]
            if (s[:i+j] == str(val1)+str(val3)) and (tail == (str(val1)+str(val3))[::-1]):
                return val1, val3, int(k)
    return None

def parse_odd(s):
    # cấu trúc: val1 + val3 + i
    # ta thử tách thành 3 số
    for i in range(1,4):
        for j in range(1,4):
            val1 = int(s[:i])
            val3 = int(s[i:i+j])
            k = s[i+j:]
            if k != "" and val1 < 128 and val3 < 128:
                return val1, val3, int(k)
    return None

res = []
for line in out_lines:
    parsed = parse_even(line)
    if parsed:
        v1,v3,idx = parsed
        res.append((idx, chr(v1), chr(v3)))
    else:
        v1,v3,idx = parse_odd(line)
        res.append((idx, chr(v1), chr(v3)))

# sort theo chỉ số xuất hiện
res.sort(key=lambda x:x[0])

flag = "".join([a+b for _,a,b in res])
print(flag)
