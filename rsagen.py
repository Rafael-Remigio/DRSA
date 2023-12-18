#!/usr/bin/python3

from src.key_gererator import KeyGenerator
import argparse
import sys



if __name__ == "__main__":
    

    # getOpts style argument parsing

    parser = argparse.ArgumentParser(
                    prog='rsagen',
                    description='Generate deterministic RSA Key pair from a password and a confusion string.',
                    epilog='')
    

    parser.add_argument('-p', '--password',help="Password String used to generate RSA Key pair",type=str)
    parser.add_argument('-c', '--confusion',help="Confusion String used for iterations on PRNG",type=str)
    parser.add_argument('-i', '--iterations',help="Number of iterations that the PRNG needs to generate confusion",type=int)

    args = parser.parse_args()


    if (args.password == None) or (args.confusion == None) or (args.iterations == None):
        parser.print_help()
        sys.exit(1)
