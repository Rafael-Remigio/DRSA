import hashlib

class HashDRBG:
    def __init__(self, seed):
        self.initial_seed = seed
        self.state = hashlib.sha256(seed).digest()
        self.counter = 0 
        self.generated_bytes = 0
        self.reseed_byte_limit = 32

    def generate(self, num_bytes):
        output = b""
        while len(output) < num_bytes:
            input_data = self.state + bytes([self.counter])
            self.state = hashlib.sha256(input_data).digest()
            output += self.state[-1:]  # Adiciona apenas o último byte ao output
            self.counter += 1
            self.generated_bytes += 1


            if self.generated_bytes == self.reseed_byte_limit :
                self.reseed()

        return output

    def reseed(self):
        self.state = hashlib.sha256(self.state + self.initial_seed).digest()
        self.generated_bytes = 0
        self.counter = 0


    def __call__(self, n):
        return self.generate(n)

if __name__ == "__main__":
    seed = b"base_seed"
    drbg = HashDRBG(seed)
    random_bytes = drbg.generate(32)  

    print(random_bytes)
