import pdb
import itertools
import time
from sage.all import *
from DataCollecctionScript import *
import numpy as np
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
crypto = Niederreiter(m, n, t)

print(f"\nCryptosystem inited - {time.time()-start}...\n")

H = crypto.H

# for i in range(1, 1001):
#     try:
#         pr_H = matrix(GF(2), [list(row) for row in list(H)][524:]).transpose().inverse()
#         print(f"Number {i} is FAILED!")
#     except ZeroDivisionError:
#         print(f"Number {i} is SUCCESS!")



