import pdb
import itertools
import time
from sage.all import *
from DataCollecctionScript import *
import numpy as np
from Niederreiter import Niederreiter
from math_utils import *

load("./GoppaCode.sage")

n = 1024
m = 10
t = 50


F_2m = GF(n, 'Z', modulus='random')
PR_F_2m = PolynomialRing(F_2m, 'X')


g_poly = GetGoppaPolynomial(PR_F_2m, t)

print("START")

start = time.time()
code = GoppaCode(n, m, g_poly)

print("SUCCESS ", time.time()-start)

H = code.parity_check_matrix()
# print((len(H), len(H[0])))

# print(len(H), len(H[0]))

msg = GetRandomMessageWithWeight(500, t)
zeros = matrix(GF(2), [0]*(n-500))

# print(new_msg)

msg = matrix(GF(2), list(zeros[0]) + list(msg[0]))
print(type(msg))
print(type(H))


## H = (code.parity_check_matrix()).transpose()
P_per = (matrix(GF(2), random_perm_matrix(n))).transpose()
S = (matrix(GF(2), random_binary_inv_matrix(m*t))).transpose()

msg = msg
H_bar = P_per*H.transpose()*S
cipher = (msg*H_bar) #.transpose()

# cipher = cipher*S
cipher = (cipher*S.inverse()).transpose()

print(cipher)

# orig_msg = list(np.array(cipher.transpose())[0])
# print(orig_msg.count(1))

# print(cipher)

print("SUCCESS")
g = code.goppa_polynomial()
X = g.parent().gen()

print()

print("Start decoding...")
start = time.time()
syndrome_poly = 0
for i in range(t):
    tmp = []
    for j in range(m):
        tmp.append(cipher[i * m + j, 0])
    # print("tmp:", tmp)  # Отладка
    # print("Length of tmp:", len(tmp))
    syndrome_poly += F_2m(tmp) * (X ** i)
            # print('syndrome_poly=', BinRepr(syndrome_poly))
recoveredtext2 = code.SyndromeDecode(syndrome_poly, 'Patterson')

recoveredtext2 = recoveredtext2*P_per.inverse()

print("Syndrome decoded: ", time.time()-start)

orig_msg = list(np.array(recoveredtext2)[0])
msg = list(np.array(msg)[0])
print(orig_msg.count(1))

print(msg==orig_msg)
print(len(list(cipher.transpose()[0])))