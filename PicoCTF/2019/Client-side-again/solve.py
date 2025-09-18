arr = [
    'getElementById',
    'value',
    'substring',
    'picoCTF{',
    'not_this',
    'f49bf}',
    '_again_e',
    'this',
    'Password Verified',
    'Incorrect password'
  ]

flag = [''] * 32
split = 4

flag[0:split*2] = arr[3]
flag[7:9] = "{n"
flag[split*2:split*2*2] = arr[4]
flag[3:6] = "oCT"
flag[split * 3 * 2: split * 4 * 2] = arr[5]
flag[6:11] = "F{not"
flag[split * 2 * 2: split * 3 * 2] = arr[6]
flag[12:16] = arr[7]

pwd = ''.join(flag)
print(pwd)