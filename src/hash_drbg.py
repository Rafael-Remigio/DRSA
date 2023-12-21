import hashlib

class HashDRBG:
    def __init__(self, seed):
        self.initial_seed = seed
        self.state = hashlib.sha256(seed).digest()
        self.counter = 1  # Inicializa o contador
        self.generated_bytes = 0

    def generate(self, num_bytes, reseed_byte_limit):
        output = b""
        while len(output) < num_bytes:
            input_data = self.state + bytes([self.counter])
            self.state = hashlib.sha256(input_data).digest()
            output += self.state[-1:]  # Adiciona apenas o último byte ao output
            self.counter += 1
            self.generated_bytes += 1

            # Se gerou y bytes, chama a função reseed
            if self.generated_bytes % reseed_byte_limit == 0:
                self.reseed()

        return output

    def reseed(self):
        self.state = hashlib.sha256(self.state + self.initial_seed).digest()

if __name__ == "__main__":
    seed = b"chave_de_semente_secreta"
    drbg = HashDRBG(seed)
    random_bytes = drbg.generate(32, 8)  

    print(random_bytes)
