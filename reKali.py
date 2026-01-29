import pdb
import itertools
import time
from sage.all import *
from DataCollecctionScript import *
from math_utils import *
from hashlib import sha3_512
import random
import string

load("./GoppaCode.sage")


def generate_random_string(length=16):
    # Определяем возможные символы: буквы (верхний и нижний регистры) и цифры
    characters = string.ascii_letters + string.digits
    # Генерируем случайную строку заданной длины
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class reKali:
    def __init__(self, m, n, t):
        self.m = m
        self.n = n
        self.t = t       
        # start = time.time()

        F_2m = None
        PR_F_2m = None
        g_poly = None
        self.code = None
        self.F_2m = None

        while True:
            try:
                F_2m = GF(n, 'Z', modulus='random')
                PR_F_2m = PolynomialRing(F_2m, 'X')
                g_poly = GetGoppaPolynomial(PR_F_2m, t)
                self.code = GoppaCode(n, m, g_poly)
                self.F_2m = F_2m
                break
            except ZeroDivisionError: continue

        self.G = self.code._G_Goppa
        self.S = matrix(GF(2), random_binary_inv_matrix(t*m)).transpose()
        self.P_per = matrix(GF(2), random_perm_matrix(n)).transpose()
        self.H = self.code.parity_check_matrix().transpose()

        # print((self.P_per*self.H*self.S))
        
        self.public_key = (self.P_per*self.H*self.S)[n-t*m:]
        self.private_key = (self.S.inverse(),
                            self.P_per.inverse(),
                            self.H)
       
        
    def encrypt(self, message):
        t = self.t
        n = self.n
        m = self.m
        
        # print(self.public_key.nrows())
        
        tmp = [t*m*[0] for i in range(n-t*m)] + [
            list(self.public_key[i]) for i in range(
                self.public_key.nrows())
            ]
        
        key = matrix(GF(2), tmp)
        
        # print(tmp)
        
        if message.count(1)!=t or len(message)!=t*m:
            assert ValueError("Incorrect lenght or wight")
        message = matrix(GF(2), (n-t*m)*[0]+message)
        return message*key
        # orig_msg = list(map(int, np.array(message)[0]))
        # print("addicted is ", orig_msg.count(1))
        
       
    
    def decrypt(self, ciphertext):
        cipher = (ciphertext*self.private_key[0]).transpose()
       
        # print(cipher)

        # print(type(cipher))
       
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
        return vector(GF(2), list(recoveredtext2[0][524:]))
    

    # def get_signature():
    #     attempt_n = 0
    #     black_list = []
    #     while True:
    #         print(f"Attempt {len(black_list)+1}")
    #         sign_base = generate_random_string()

    #         if sign_base in black_list: continue

    #         hash = sha3_512(usedforsecurity=True)
    #         hash.update(sign_base.encode())
    #         hash_res = hash.hexdigest()


    #         hash_res_bin = list(bin(int(hash_res, 16))[2:].zfill(512))[:500]
    #         synd = matrix(GF(2), [[int(i) for i in hash_res_bin]])
                
    #             # g = self.code.goppa_polynomial()
    #             # X = g.parent().gen()
                
    #             # syndrome_poly = 0
    #             # for i in range(t):
    #             #     tmp = []
    #             #     for j in range(m):
    #             #         tmp.append(synd[i * m + j, 0])
    #             #     # print("tmp:", tmp)  # Отладка
    #             #     # print("Length of tmp:", len(tmp))
    #             #     syndrome_poly += self.F_2m(tmp) * (X ** i)
    #             #             # print('syndrome_poly=', BinRepr(syndrome_poly))
    #             # signature = self.code.SyndromeDecode(syndrome_poly, 'Patterson')
    #         signature =self.decrypt(synd)

    #         # print(self.encrypt([int(signature[i]) for i in range(signature.length())]))

    #         # print(synd)

    #         wt = 0
    #         for i in range(signature.length()): wt += int(signature[i])
    #         if wt==50 and self.encrypt([int(signature[i]) for i in range(signature.length())])==synd:
    #             return signature
    #         else:
    #             black_list.append(sign_base)
    #             # continue
            
    #         # except: continue

