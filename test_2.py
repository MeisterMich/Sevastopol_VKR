import pdb
import itertools
import time
from sage.all import *
from DataCollecctionScript import *
import numpy as np
from reKali import reKali
from Niederreiter import Niederreiter
from math_utils import *
import matplotlib.pyplot as plt

from decimal import Decimal

def get_size(sage_matr):
    return sage_matr.nrows(), sage_matr.ncols()

n = 1024
m = 10
t = 50

encrypt_stat = []
decrypt_stat = []

start = time.time()
crypto = reKali(m, n, t)
print(time.time()-start)

print("Cryptosystem inited...")

# msg = list(np.array(GetRandomMessageWithWeight(t*m, t))[0])
# start = time.time()
# ciphertext = crypto.encrypt(msg)

# # print(ciphertext.ncols())

# o_text = crypto.decrypt(ciphertext)

# print()
# print(o_text, vector(GF(2), msg))

decrypt_stat = []
encrypt_stat = []
init_stat = []

for i in range(1000):
    msg = list(np.array(GetRandomMessageWithWeight(t*m, t))[0])
    start = time.time()
    ciphertext = crypto.encrypt(msg)
    encrypt_stat.append(time.time()-start)
    
    start = time.time()
    orig = crypto.decrypt(ciphertext)
    decrypt_stat.append(time.time()-start)

print(f"Среднее время шифрования: {sum(encrypt_stat)/len(encrypt_stat)}\n")
print(f"Среднее время дешифрования: {sum(decrypt_stat)/len(decrypt_stat)}\n")

plt.plot(encrypt_stat, color='red')
plt.plot(decrypt_stat, color='black')
plt.show()

print(f"\nРазмерность матрицы перестановки: {crypto.P_per.nrows()}x{crypto.P_per.ncols()}")
# print(crypto.P_per)

print(f"\nРазмерность матрицы S: {crypto.S.nrows()}x{crypto.S.ncols()}")
# print(crypto.S)

# print("\nG:")
# print(crypto.G)

print(f"\nРазмерность матрицы H^T: {crypto.H.nrows()}x{crypto.H.ncols()}")
# print()

print(f"\nРазмерность матрицы Hpub: {crypto.public_key.nrows()}x{crypto.public_key.ncols()}")
# print(crypto.public_key)

# H = crypto.public_key

# print(msg)
# print(H.nrows())



# G_str = [row for row in list(crypto.code._G_Goppa)]

# f = open('text.txt', 'a+')
# for row in G_str:
#     f.write(' '.join(map(str, row))+"\n")



    
            
        


# msg = np.array(GetRandomMessageWithWeight(t*m, t))[0]
# msg = list(map(int, msg))

# print()
# print(f"Размерность матрицы S: {get_size(crypto.private_key[0])[0]}x{get_size(crypto.private_key[0])[1]}\n")
# print(f"Размерность матрицы перестановки: {get_size(crypto.private_key[1])[0]}x{get_size(crypto.private_key[1])[1]}\n")
# print(f"Размерность матрицы H^T: {get_size(crypto.private_key[2])[0]}x{get_size(crypto.private_key[2])[1]}\n")
# print(f"Размерность матрицы Hpub: {get_size(crypto.public_key)[0]}x{get_size(crypto.public_key)[1]}\n")