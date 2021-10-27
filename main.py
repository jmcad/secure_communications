from diffie_hellman import DH
from rc4 import RC4
import sdes

if __name__ == "__main__":
    # create objects for alice and bob
    KEY = '11100101010110'
    e = sdes.encrypt(KEY, '01001000')
    d = sdes.decrypt(KEY, e)
    print("Ciphertext: ", e)
    print("Plaintext: ", d)
    print(chr(199))