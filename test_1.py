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

load("./GoppaCode.sage")

t = 50
m = 11
n = 1024*2

encoding_stat = []
decoding_stat = []


start = time.time()
F_2m = GF(n, 'Z', modulus='random')
PR_F_2m = PolynomialRing(F_2m, 'X')
g_poly = GetGoppaPolynomial(PR_F_2m, t)
code = GoppaCode(n, m, g_poly)
# encoding_stat.append(gen_time)
print("Time spent", time.time()-start)

message = GetRandomMessage(code.generator_matrix().nrows())
    
# print(i)
    

codeword = code.Encode(message)
# gen_time  = time.time() - start

    
    
    
error = GetRandomMessageWithWeight(code.generator_matrix().ncols(), t)
codeword = codeword + error
    
    
start = time.time()
recoveredtext1 = code.Decode(codeword, 'Euclidean')

