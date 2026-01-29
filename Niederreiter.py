import pdb
import itertools
import time
from sage.all import *
from DataCollecctionScript import *
from math_utils import *

load("./GoppaCode.sage")

class Niederreiter:
    def __init__(self, m, n, t):
        self.m = m
        self.n = n
        self.t = t       
        # start = time.time()

        flag = True
        while flag:
            try:
                F_2m = GF(n, 'Z', modulus='random')
                PR_F_2m = PolynomialRing(F_2m, 'X')
                g_poly = GetGoppaPolynomial(PR_F_2m, t)
                self.code = GoppaCode(n, m, g_poly)
                self.F_2m = F_2m
                flag^=1
            except:
                pass
        
        self.G = self.code._G_Goppa
        self.S = matrix(GF(2), random_binary_inv_matrix(t*m)).transpose()
        self.P_per = matrix(GF(2), random_perm_matrix(n)).transpose()
        self.H = self.code.parity_check_matrix().transpose()
        
        self.public_key = self.P_per*self.H*self.S
        self.private_key = (self.S.inverse(),
                            self.P_per.inverse(),
                            self.H)
       
        
    def encrypt(self, message):
        t = self.t
        n = self.n
        m = self.m
        if message.count(1)!=t or len(message)!=t*m:
            assert ValueError("Incorrect lenght or wight")
        message = matrix(GF(2), (n-t*m)*[0]+message)
        return message*self.public_key
        # orig_msg = list(map(int, np.array(message)[0]))
        # print("addicted is ", orig_msg.count(1))
        
       
    
    def decrypt(self, ciphertext):
        cipher = (ciphertext*self.private_key[0]).transpose()
       
        # print(cipher)
       
        m = self.m
        n = self.n
        t = self.t
       
        g = self.code.goppa_polynomial()
        X = g.parent().gen()
        
        syndrome_poly = 0
        for i in range(t):
            tmp = []
            for j in range(m):
                tmp.append(cipher[i * m + j, 0])
            # print("tmp:", tmp)  # Отладка
            # print("Length of tmp:", len(tmp))
            syndrome_poly += self.F_2m(tmp) * (X ** i)
                    # print('syndrome_poly=', BinRepr(syndrome_poly))
        recoveredtext2 = self.code.SyndromeDecode(syndrome_poly, 'Patterson')

        recoveredtext2 = recoveredtext2*self.private_key[1]
        return list(map(int, list(recoveredtext2[0][524:])))