def rc4(key, n):
    # Key Scheduling Algorithm
        S = list()
        T = list()  # temporary array
        j = 0

        # Initialization
        for i in range(256):
            S.append(i)
            T.append(key[i % len(key)])
            # S[i] = i
            # T[i] = key[i % len(key)]
        
        # Initial Permutation of S
        for i in range(256):
            j = (j + S[i] + T[i]) % 256
        
            # Swap
            S[i], S[j] = S[j], S[i]

    # Pseudo Random Number Generator Algorithm
        i = 0
        j = 0
        K = list()

        while n > 0:
            n -= 1
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            
            # Swap
            S[i], S[j] = S[j], S[i]

            t = (S[i] + S[j]) % 256
            K.append(S[t])
        return K 