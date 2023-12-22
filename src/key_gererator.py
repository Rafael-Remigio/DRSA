from argon2 import PasswordHasher

# Password based key generation
# Using argon2 instead of PBKDF2. Winner of https://www.password-hashing.net/
# Why argon argon2: 
# argon2 is not just compute-bounded but also memory bounded. 
# This means that - for the same unlock time for you - password cracking will be significantly slower 
# for an attacker attempting to crack your password on a GPU or ASIC, because an attacker cannot run as 
# many instances of argon2 in parallel on a GPU, as they could with PBKDF2 due to memory limitations. 
# This means that for the same unlock time for the user, password cracking becomes orders of magnitude 
# slower compared to pbkdf2.

class KeyGenerator():

    def __init__(self):
        # Initialize the PasswordHasher
        self.password_hasher = PasswordHasher(hash_len=32)

        return

    """Generate [key] from a string [password], integer [number_iterations], and [confusion_bytes]"""
    def generate_key_from_password(self,password:str,number_iterations:int,confusion_bytes: bytes) -> bytes:

        # Use the confusion_bytes and number of iterations as a salt.
        # confusion_bytes = b'confusion' and number_iterations = 3
        # b'confusion\x03\x00\x00\x00\x00\x00\x00\x00'
        salt = confusion_bytes +  number_iterations.to_bytes(length=8,byteorder='little')

        return self.password_hasher.hash(password=password,salt=salt)
    