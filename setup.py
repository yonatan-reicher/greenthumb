#!/usr/bin/python

import sys, os
import os.path
from pathlib import Path

def create(isa,c,filename,lang):
    
    out_path = Path(isa) / f"{isa}-{c}.rkt"
    if os.path.isfile("template/"+c+".rkt"):
        filename = "template/"+c+".rkt"
        fin = open(filename,"r")
        text = fin.read().replace("$-",isa+"-")
        out_path.write_text(text)
        fin.close()
    else:
        fin = open(filename,"r")
        text = fin.read().replace("$1",isa).replace("$2",c)
        out_path.write_text(f'#lang {lang}\n{text}')
        fin.close()

def main(isa):
    print("Create template files for", isa)
    os.system("mkdir " + isa)

    for name in ["test-simulator.rkt", "test-search.rkt", "main.rkt", "optimize.rkt"]:
        text = input_path.read_text().replace('$', isa)
        output_path.write_text(text)

    # racket
    for c in ["machine", "simulator-racket"]:
        create(isa,c,"template/class-constructor.rkt","racket")
        
    for c in ["parser", "printer", "stochastic", "forwardbackward"]:
        create(isa,c,"template/class.rkt","racket")
        
        
    # # rosette
    for c in ["simulator-rosette", "validator"]:
        create(isa,c,"template/class-constructor.rkt","s-exp rosette")
        
    for c in ["symbolic", "inverse", "enumerator"]:
        create(isa,c,"template/class.rkt","s-exp rosette")

if __name__ == "__main__":
    main(sys.argv[1])
