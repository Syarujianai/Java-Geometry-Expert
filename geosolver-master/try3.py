import pickle


with open('match_char.pk', 'rb') as f:
    match_chars = pickle.load(f)

# print(len(match_chars))
knt = 0
for chars in match_chars:
    knt += len(chars)

# for char in match_chars:
# print(knt/len(match_chars))
# 3 chars
