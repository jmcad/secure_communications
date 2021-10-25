P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]

# Substitution Tables
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

IP = [2, 6, 3, 1, 4, 8, 5, 7] # initial permutation
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6] # inverse permutation
EP = [4, 1, 2, 3, 2, 3, 4, 1] # expansion permutaion

#KEY = '1010000010'
#KEY = '1111111111'

def permutate(rawkey, ptable):
    new = ''
    for i in ptable:
        new += rawkey[i - 1]
    return new

def split_left(array):
    left_half = array[:(len(array)//2)]
    return left_half

def split_right(array):
    right_half = array[(len(array)//2):]
    return right_half

# left shift 1 position
def left_shift(array):
    shifted_array = array[1:] + array[:1]
    return shifted_array

# left shift 2 positions
def left_shift2(array):
    shifted_array2 = left_shift(left_shift(array))
    return shifted_array2

def key_gen1(key):
    k = permutate(key, P10)
    lh = left_shift(split_left(k))
    rh = left_shift(split_right(k))
    ls1 = lh + rh
    k1 = permutate(ls1, P8)
    return k1, lh, rh

def key_gen2(key):
    lh2 = left_shift2(key_gen1(key)[1])
    rh2 = left_shift2(key_gen1(key)[2])
    ls2 = lh2 + rh2
    k2 = permutate(ls2, P8)
    return k2

def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new

def lookup(key, stable):
    row = int(key[0] + key[3], 2)
    col = int(key[1] + key[2], 2)
    return '{0:02b}'.format(stable[row][col])

def fk(bits, key):
    lh = split_left(bits)
    rh = split_right(bits)
    bits = permutate(rh, EP)
    bits = xor(bits, key)
    bits = lookup(split_left(bits), S0) + lookup(split_right(bits), S1)
    bits = permutate(bits, P4)
    return xor(bits, lh)

def encrypt(key, plaintext):
    ip = permutate(plaintext, IP)
    data = fk(ip, key_gen1(key)[0])
    swap = split_right(ip) + data
    fp = fk(swap, key_gen2(key))
    return permutate(fp + data, IP_INVERSE)


def decrypt(key, ciphertext):
    ip = permutate(ciphertext, IP)
    data = fk(ip, key_gen2(key))
    swap = split_right(ip) + data
    fp = fk(swap, key_gen1(key)[0])
    return permutate(fp + data, IP_INVERSE)

if __name__ == "__main__":
    KEY = '0000000000'
    e = encrypt(KEY, '10101010')
    d = decrypt(KEY, e)
    print("Ciphertext: ", e)
    print("Plaintext: ", d)