import argparse
from errors import Syntaxerror, Extensionerror, Miscerror, terminate

def getcliargs() -> str:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("FILENAME", help="filename you wish to run")
    args = argparser.parse_args()
    result = ""
    with open(args.FILENAME, "r") as f:
        result = f.read()
    
    if not args.FILENAME.endswith(".bwt"):
        print(Extensionerror(result, "Change the file extension"))
        terminate()
    return result
