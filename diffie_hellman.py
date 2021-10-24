class DiffieHellman:
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
    
    def gen_key(self):
        x = self.public_key1**self.private_key % self.public_key2
        return x
    
    def gen_secret(self, gpk):
        k = gpk**self.private_key % self.public_key2
        return k
    