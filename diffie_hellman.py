class DH:
    def __init__(self, randint, prime, private_key):
        self.randint = randint                  # g
        self.prime = prime                      # p
        self.private_key = private_key          
    
    def gen_pubkey(self):
        x = (self.randint**self.private_key) % self.prime
        return x
    
    def gen_secret(self, public_key):
        k = (public_key**self.private_key) % self.prime
        return k
    