# python .\main.py -f .\input.bfr -r
# python .\main.py -f .\input.bfr -toc -runcc

from src.generator import Generator
from src.parseur import Parseur
from src.lexer import Lexer
import argparse
import time
import os

parser = argparse.ArgumentParser(description='Interpreteur de code')
parser.add_argument('-f', '--file', help='fichier à interpreter', required=True)
parser.add_argument('-d', '--debug', help='mode debug', required=False, action='store_true')
parser.add_argument('-di', '--debuginterpreteur', help='mode debug', required=False, action='store_true')
parser.add_argument('-rc', '--runc', help='mode debug', required=False, action='store_true')
parser.add_argument('-rp', '--runp', help='mode debug', required=False, action='store_true')
parser.add_argument('-stfu', '--stfu', help='mode debug', required=False, action='store_true')
parser.add_argument('-c', '--clean', help='sans commentaires', required=False, action='store_true')
args = parser.parse_args()

code = open(args.file, "r").read()

if not args.stfu : print("[INFO] : Génération du code")
t = time.time()
parseur = Parseur(args.debug)
code = parseur.parse(code)
lexer = Lexer(args.debug)
lexer.parse(code)
instructions = lexer.instructions
generator = Generator(args.debug)
generator.generate(instructions)
instructions = generator.instructions
if args.clean:
    instructions = "".join(x for x in list(instructions) if x in "+-<>[].,")
with open("sortie.bf", "w") as f:
    f.write(instructions)
if not args.stfu : print(f"[INFO] : Génération du code terminée en {time.time() - t} secondes")

if not args.stfu : print("[INFO] : Execution du code")

t = time.time()
if args.runc:
    os.system("./src/interpreteur.exe ./sortie.bf")
if args.runp:
    from src.interpreteur import interpreter
    interpreter(instructions, args.debuginterpreteur)
        
if not args.stfu : print(f"[INFO] : Execution du code terminée en {time.time() - t} secondes")