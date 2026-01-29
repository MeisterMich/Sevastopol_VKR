from reKaki import reKali
from time import time
from DataCollecctionScript import GetRandomMessageWithWeight
import numpy as np

m = 10
n = 1024
t = 50

print("Cryptosystem initialization...")
start = time()

crypto = reKali(10, 1024, 50)

print(f"Cryptosystem inited, time spent - {time()-start}")

msg = list(np.array(GetRandomMessageWithWeight(t*m, t))[0])

cipher =  crypto.encrypt(msg)

print(crypto.public_key.inverse())


# print(cipher)
# recv = crypto.decrypt(cipher)

# print(msg==recv)