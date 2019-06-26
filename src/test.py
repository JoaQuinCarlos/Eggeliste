a = {}
b = {}
c = {}

a['Svein Ingar'] = 13.0
a['John'] = 8.0

b['Svein Ingar'] = 650.0
b['John'] = 300.0

for k, v in a.items():
    print(v)
    c[k] = b[k] / v

score_arr = sorted(((v, k) for k, v in c.items()), reverse=True)

for v, k in score_arr:
    print("%s: %f" % (k, v))
