from reKali import reKali
from time import time
from DataCollecctionScript import GetRandomMessageWithWeight
import numpy as np
from hashlib import sha3_512
from sage.all import *

def save_binary_matrix_to_file(matr, filename):    
    # Открываем файл для записи
    with open(filename, 'a+') as f:
        # Записываем матрицу в файл
        for row in matr:
            f.write(' '.join(map(str, row)) + '\n')


m = 10
n = 1024
t = 50

cr = reKali(m, n, t)

pub = cr.public_key

# print(pub)
# save_binary_matrix_to_file(pub, 'pub.key')
sign = cr.get_signature()
# print(sign[0])
sign_list = [int(sign[i]) for i in range(sign.length())]



print(sign_list)