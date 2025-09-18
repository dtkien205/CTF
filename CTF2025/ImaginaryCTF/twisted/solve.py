import numpy as np
import string

# Các vector 3D từ output (bỏ cột đầu tiên)
Y = np.array([
    (81.37080239, -143.96234736, 123.95164171),
    (100.91788802, -135.90959582, 146.37617105),
    (49.20197906, -155.2459834 ,  73.56498047),
    (49.36829422, -117.25335109, 181.11592151),
    (-12.0765699 , -126.07584525, 125.88335439),
    (40.78304285,  -51.15180044, 143.18760932),
    (48.04296984, -128.92087521,  68.4732401 ),
    (-0.41865393, -53.94228136, 100.98194223),
    (27.56200727, -52.57316992,  44.05723383),
    (60.67582903, -76.44584757,  40.88253203),
])

s = 1.25  # scale đã dùng khi encode

# Chunk 0 trong plaintext: "ict"
x0 = np.array([ord('i'), ord('c'), ord('t')], dtype=float)

# Hàm tính R,t (Kabsch algorithm với scale)
def kabsch_with_scale(X, Y, scale):
    Xc = X - X.mean(axis=0, keepdims=True)
    Yc = Y - Y.mean(axis=0, keepdims=True)
    H = (Yc.T @ Xc)
    U, Svals, Vt = np.linalg.svd(H)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        Vt[-1,:] *= -1
        R = U @ Vt
    t = Y.mean(axis=0) - scale*(R @ X.mean(axis=0))
    return R, t

def decode_all(R, t):
    X_est = (R.T @ (Y.T - t.reshape(3,1))) / s
    X_est = X_est.T
    Xr = np.rint(X_est).astype(int)
    return Xr

# Vì dữ liệu có nhiễu, ta cần giả sử thêm 2 điểm nữa:
# chunk1 phải là 'f{?'
# chunk9 phải kết thúc bằng '}00'
X_known = np.array([
    [ord('i'), ord('c'), ord('t')],
    [ord('f'), ord('{'), ord('q')],   # ký tự thứ 3 đoán gần đúng
    [ord('}'), ord('0'), ord('0')]
], dtype=float)

Y_known = np.stack([Y[0], Y[1], Y[9]], axis=0)

# Tính R,t từ 3 điểm cố định
R, t = kabsch_with_scale(X_known, Y_known, s)

# Giải toàn bộ
Xr = decode_all(R, t)

# Chuyển thành chuỗi
flag = ''.join(''.join(map(chr, tri)) for tri in Xr)
flag = flag.replace("00", "")  # bỏ padding

print("Recovered flag:", flag)
