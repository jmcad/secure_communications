class RC4:
    # Key Scheduling Algorithm
    def ksa(key):
        S = [None]*256
        T = [None]*256
        j = 0

        # Initialization
        for i in range(256):
            S[i] = i
            T[i] = key[i % len(key)]
        
        # Initial Permutation of S
        for i in range(256):
            j = (j + S[i] + T[i]) % 256
            
            # Swap
            S[i], S[j] = S[j], S[i]

            return S

    # Pseudo Random Number Generator Algorithm
    def prng(S):
        i, j = 0
        k = []

        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            
            S[i], S[j] = S[j], S[i]

            t = (S[i] + S[j]) % 256
            k.append(S[t])
            return k  