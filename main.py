from diffie_hellman import DH
import csprng, sdes

p = 7

def getG(p):
    for x in range(1, p):
        rand = x
        exp = 1
        next = rand % p

        while (next != 1):
            next = (next*rand) % p
            exp += 1
        
        if exp == p-1:
            print(rand)

def main():
    # public parameters used
    shared_base = 5     # g
    shared_prime = 23   # p

    alice_private = int(input("Alice, choose a private key: "))     # a
    bob_private = int(input("Bob, choose a private key: "))
    print()         # b

    # create objects for alice and bob
    alice = DH(shared_base, shared_prime, alice_private) #randint, prime, private key
    bob = DH(shared_base, shared_prime, bob_private)  #randint, prime, private key

    print("Public Parameters")
    print(f"    Public Base: {shared_base}")
    print(f"    Public Prime: {shared_prime}\n")


    # Begin
    x_alice = alice.gen_pubkey()
    x_bob = bob.gen_pubkey()
    print("Alice and Bob sends their generated public keys to \neach other over the channel...")
    print(f"    Alice's public key: {x_alice}")
    print(f"    Bob's public key: {x_bob}\n")

    k_alice = alice.gen_secret(x_bob)
    k_bob = bob.gen_secret(x_alice)
    print("Calculated shared key:")
    print(f"    Alice's shared key: {k_alice}")
    print(f"    Bob's shared key: {k_bob}\n")

    decimaltobinary = bin(k_alice).replace("0b", "")
    new_key = [ord(c) for c in decimaltobinary]
    keystream = csprng.rc4(new_key, 2)
    print(f"Keystream\n    Decimal: {keystream}")

    keystream = [bin(k).replace("0b", "") for k in keystream]   # convert keystream to binary
    print(f"    Binary: {keystream}\n")

    #secret key K
    K = ''.join(keystream)
    print(f"Secret key: {K}\n")


    # sdes encryption, decryption
    plaintext = ['01001000', '01100101', '01101100', '01101100', 
            '01101111', '00100000', '01010111', '01101111', 
            '01110010', '01101100', '01100100', '00100001']
    ciphertext = []
    for x in plaintext:
        ciphertext.append(sdes.encrypt(K, x))
    print(ciphertext)

    decipheredtext = []
    for x in ciphertext:
        decipheredtext.append(sdes.decrypt(K, x))
    print(decipheredtext)

    for i, x in enumerate(decipheredtext):
        decipheredtext[i] = chr(int(x, 2))
    
    result = ''.join(decipheredtext)
    print(result)


if __name__ == "__main__":
    main()
