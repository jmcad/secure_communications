from diffie_hellman import DH
import csprng, sdes

def main():
    # global g and p agreed by both parties
    common_base = 5     # g
    common_prime = 23   # p

    alice_private = int(input("Alice, choose a private key: "))     # a
    bob_private = int(input("Bob, choose a private key: "))         # b
    print()         

    # create objects for alice and bob
    alice = DH(common_base, common_prime, alice_private) #random integer, prime, private key
    bob = DH(common_base, common_prime, bob_private)  #random integer, prime, private key

    print("Global Public Parameters")
    print(f"    Public Base: {common_base}")
    print(f"    Public Prime: {common_prime}\n")


    # Begin
    x_alice = alice.gen_pubkey()
    x_bob = bob.gen_pubkey()
    print("Alice and Bob sends their generated public keys to \neach other over the channel...")
    print(f"    Alice's public key: {x_alice}")
    print(f"    Bob's public key: {x_bob}\n")

    k_alice = alice.gen_secret(x_bob)
    k_bob = bob.gen_secret(x_alice)
    print("Calculated shared key...")
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
    plaintext = '010010000110010101101100011011000110111100100000010101110110111101110010011011000110010000100001'
    # plaintext = input("")

    split_strings = []
    n = 8
    for i in range(0, len(plaintext), n):
        split_strings.append(plaintext[i : i + n])
    
    ciphertext = []
    for x in split_strings:
        ciphertext.append(sdes.encrypt(K, x))
    string_ct = "".join(ciphertext)


    decipheredtext = []
    for x in ciphertext:
        decipheredtext.append(sdes.decrypt(K, x))

    for i, x in enumerate(decipheredtext):
        decipheredtext[i] = chr(int(x, 2))
    
    for i, x in enumerate(ciphertext):
        ciphertext[i] = chr(int(x, 2))
    string_ct_ascii = "".join(ciphertext)

    result = "".join(decipheredtext)
    print(f"Plain binary text: {plaintext}")
    print()
    print("Encrypting using SDES...\n")
    print(f'Cipheredtext: {string_ct}')
    print(f'Cipheredtext ascii: {string_ct_ascii}\n')
    print("Decrypting using SDES...\n")
    print(f"Original text in ASCII: {result}")


if __name__ == "__main__":
    main()
