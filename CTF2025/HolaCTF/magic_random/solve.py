import random

def unshuffle(target, seed):
    n = len(target)
    idx = list(range(n))
    random.seed(seed)
    random.shuffle(idx)
    S = ["?"]*n
    for j, orig_pos in enumerate(idx):
        S[orig_pos] = target[j]
    return "".join(S)

target = "{{99-85}}"

for seed in range(6):  # demo cho seed 0–5
    print(f"{unshuffle(target, seed)}")
