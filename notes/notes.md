# Notes - Interpretation and resume of the assignment pdf

RSA key pairs are randomly generated for some dimension of their module.

Alternatively, one can use a deterministic key pair generation. In this case, the same key pair is always
generated from a set of parameters, a deterministic and secure RSA key pair generation.

**State of the Art**
* Devices such as a TPM (Trusted Platform Module), which exist in most laptops today, are able to recreate RSA key pair this exact way, i.e. from some user-provided secret. 
* https://crypto.stackexchange.com/questions/1662/how-can-one-securely-generate-an-asymmetric-key-pair-from-a-short-passphrase/1665#1665
* https://github.com/joekir/deterministics
* https://crypto.stackexchange.com/a/24517


Implement Generating RSA Key pair

* https://github.com/Biggy54321/crypto-rsa-C/blob/master/rsa_key_gen.c
* https://stackoverflow.com/questions/18264314/generating-a-public-private-key-pair-using-an-initial-key#answer-18266970


A TPM also uses something that is not easily available to an ordinary program: an internal secret, unique to the TPM device

Make the process slow, so that guessing attacks against the secrets that seed the D-RSA process could not thrive. Also make it so no parallel machines or precomputation databases could be used.

## Todo

* A pseudo-random byte generator, with a N -byte seed. The initialization of this generator will
be the fundamental contribution to the time to generate a D-RSA key pair

* A complete, and secure, RSA key pair generator using some arbitrary precision integer represen-
tation.


**3 paremeter used** - must assure that the setup of a randomness source for the RSA key pair generator takes a long time
* a password
* a confusion string
* an iteration count


### Pseudo-random byte generator

Consider, for instance, using the generator of a stream cipher.

* Compute a bootstrap seed from the password, the confusion string and the iteration count. Algorithms to use (Argon2, Scrypt, PBKDF2)

* transform the confusion string into an equal length sequence of bytes. 

* Initialize the generator with the bootstrap seed;

* Use the generator to produce a pseudo-random stream of bytes, stopping when the confusion pattern is found;

* Use the generator to produce a new seed and use that seed to re-initialize the generator

* Repeat the last two steps as many times as the number of iterations defined by the user

**Pseudo code:**
```
byte[] seed = PBKDF2(password + confusion_string + iteration_count);

byte[] confusion_pattern = confusion_string.encode("utf-8");

PseudoRandomGenerator g = PseudoRandomGenerator(seed);

int count = 0;

byte[] current_sequence = bytes.zeros(confusion_pattern.lenght);

while (count < iteration_count):

    current_sequence[] = g.random_sequence(confusion_pattern.lenght);

    if current_sequence == confusion_pattern:
        count += 1;
        new_seed = g.random_sequence(seed.length);

        g = PseudoRandomGenerator(new_seed);

int rsa_generator_key_length = 32
byte[] rsa_seed = g.random_sequence(rsa_generator_key_length)

exponent = 2**16 + 1

RSAGenerator rsa_g = RSAGenerator(rsa_seed,exponent);

rsa_g.getPriv();
rsa_g.getPub();

```

This strategy can take an arbitrarily high computation time by acting either on the length of the
confusion string and on the number of iterations


### Applications

**randgen** - evaluating the time taken to set up the described pseudo-random generator for diferent input parameters. rsagen using the stdin as random byte source. This allows you to experiment your application with many different randomness sources (e.g. /dev/urandom or other) just by redirecting the application's stdin. 

**rsagen** - uses it to deterministically to generate an RSA key pair.



# Links

* https://crypto.stackexchange.com/questions/1662/how-can-one-securely-generate-an-asymmetric-key-pair-from-a-short-passphrase/1665#1665
* https://github.com/joekir/deterministics
* https://crypto.stackexchange.com/a/24517
* https://github.com/Biggy54321/crypto-rsa-C/blob/master/rsa_key_gen.c
* https://stackoverflow.com/questions/18264314/generating-a-public-private-key-pair-using-an-initial-key#answer-18266970
* https://www.schneier.com/academic/fortuna/

* https://github.com/pycrypto/pycrypto/tree/master/lib/Crypto/Random/Fortuna

# Code snippets

## Fortuna python implementation
https://www.researchgate.net/publication/215858122_Fortuna_Cryptographically_Secure_Pseudo-Random_Number_Generation_In_Software_And_Hardware

Fortuna possible improvments found in 2015 - https://eprint.iacr.org/2014/167

python code - https://github.com/pycrypto/pycrypto/tree/master/lib/Crypto/Random/Fortuna

## Generating a RSA Key deterministically in python3

The PRNG (pseudo-random number generator) could be changed to use another PRNG

```
from Crypto.PublicKey import RSA
from Crypto.Hash import HMAC
from struct import pack

# The first key could also be read from a file
first_key = RSA.generate(2048)

# Here we encode the first key into bytes and in a platform-independent format.
# The actual format is not important (PKCS#1 in this case), but it must
# include the private key.
encoded_first_key = first_key.exportKey('DER')

seed_128 = HMAC.new(encoded_first_key + b"Application: 2nd key derivation").digest()

class PRNG(object):

  def __init__(self, seed):
    self.index = 0
    self.seed = seed
    self.buffer = b""

  def __call__(self, n):
    while len(self.buffer) < n:
        self.buffer += HMAC.new(self.seed +
                                pack("<I", self.index)).digest()
        self.index += 1
    result, self.buffer = self.buffer[:n], self.buffer[n:]
    return result

second_key = RSA.generate(2048, randfunc=PRNG(seed_128))
```

# Pseudo Random Generator


If a user or application asks for random data, the generator runs its
algorithm and generates pseudorandom data. Now suppose an attacker
manages to compromise the generator’s state after the completion of the
request. It would be nice if this would not compromise the previous results
the generator gave. Therefore, after every request we generate an extra 256
bits of pseudorandom data and use that as the new key for the block cipher.
We can then forget the old key, thereby eliminating any possibility of leaking
information about old requests.

To ensure that the data we generate will be statistically random, we can-
not generate too much data at one time. After all, in purely random data
there can be repeated block values, but the output of counter mode never
contains repeated block values.