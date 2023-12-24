#!/usr/bin/python3

from src.key_gererator import KeyGenerator
import argparse
import sys
import base64
from src.hash_drbg import HashDRBG
from Crypto.PublicKey import RSA

if __name__ == "__main__":
    

    # getOpts style argument parsing

    parser = argparse.ArgumentParser(
                    prog='rsagen',
                    description='Generate deterministic RSA Key pair from a password a confusion string and the nunber of iterations',
                    epilog='')
    

    parser.add_argument('-p', '--password',help="Password String used to generate RSA Key pair",type=str)
    parser.add_argument('-c', '--confusion',help="Confusion String used for iterations on PRNG",type=str)
    parser.add_argument('-i', '--iterations',help="Number of iterations that the PRNG needs to generate confusion",type=int)

    parser.add_argument('-o', '--private',help="Private key output file - PEM format",type=str)
    parser.add_argument('-f', '--public',help="Public key output file - PEM format",type=str)

    args = parser.parse_args()



    if (args.password == None) or (args.confusion == None) or (args.iterations == None):
        parser.print_help()
        sys.exit(1)

    password = args.password
    confusion_string = args.confusion
    iterations = args.iterations

    # encode confusion string into bytes
    confusion_bytes = confusion_string.encode('utf8')

    # Generate key from password
    key_generator = KeyGenerator()
    argon_key = key_generator.generate_key_from_password(password=password,confusion_bytes=confusion_bytes,number_iterations=iterations)
    

    # Split the argol byte key and retrieve just the hash. remove the salt and other stuff. 
    base_seed = argon_key.split("$")[-1]

    # Decode the key/seed (i need to add the = because of the base64 padding). 
    base_seed_bytes = base64.b64decode(base_seed + "=")

    pnrg = HashDRBG(base_seed_bytes)


    count = 0
    len_confusion_bytes = len(confusion_bytes)
    while (count < iterations):

        generated_bytes = pnrg.generate(len_confusion_bytes)

        if generated_bytes == confusion_bytes:

            count += 1

            new_seed = pnrg.generate(len(base_seed_bytes))

            pnrg = HashDRBG(new_seed)

    rsa_key_pair = RSA.generate(2048, randfunc=pnrg,)

    pv_key_string = rsa_key_pair.exportKey()
    pb_key_string = rsa_key_pair.public_key().exportKey()

    if (args.private != None):
        with open (args.private , "w") as prv_file:
            print("{}".format(pv_key_string.decode()), file=prv_file)

    if (args.public != None):
        with open (args.public , "w") as pb_file:
            print("{}".format(pb_key_string.decode()), file=pb_file)