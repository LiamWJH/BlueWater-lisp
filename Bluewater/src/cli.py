import argparse
from errors import Sytaxerror, Extensionerror, Miscerror

def getcliargs() -> str:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("FILENAME", help="filename you wish to run")
    args = argparser.parse_args()
    result = ""
    with open(args.FILENAME, "r") as f:
        result = f.read()
    
    return result
