import os,sys,re
import collections
import argparse
import numpy as np
from pathlib import Path
from TPEA import parsers
def main():
    args = parsers.parse_args(sys.argv[1:])
    if args.command == "SRRHISAT":
        from TPEA.classify import SRRHISAT
        try:
            SRRHISAT(args.SRR,args.SILVA,args.CPU,args.miniLen)
        except:
            sys.exit(1)
    elif args.command == "SRRHISATSIN":
        from TPEA.classify import SRRHISATSIN
        try:
            SRRHISATSIN(args.SRR,args.SILVA,args.CPU,args.miniLen)
        except:
            sys.exit(1)
    elif args.command == "HISATLOCAL":
        from TPEA.classify import HISATLOCAL
        try:
            HISATLOCAL(args.SRR,args.SILVA,args.CPU)
        except:
            sys.exit(1)
    elif args.command == "HISATFA":
        from TPEA.classify import HISATFA
        try:
            HISATFA(args.SRR,args.SILVA,args.CPU)
        except:
            sys.exit(1)
    elif args.command == "MAP16S":
        from TPEA.classify import SRRCLASS
        try:
            SRRCLASS(args.SRR,args.TaxB,args.RefID)
        except:
            sys.exit(1)
    elif args.command == "MAP16SSIN":
        from TPEA.classify import SRRCLASSSIN
        try:
            SRRCLASSSIN(args.SRR,args.TaxB,args.RefID)
        except:
            sys.exit(1)
    elif args.command == "MAPN":
        from TPEA.classify import MAPN
        try:
            MAPN(args.SRR,args.TaxB,args.RefID)
        except:
            sys.exit(1)
    elif args.command == "SAMC1FQ":
        from TPEA.classify import SAMC1FQ
        try:
            SAMC1FQ(args.SRR)
        except:
            sys.exit(1)
if __name__=='__main__':
    main()