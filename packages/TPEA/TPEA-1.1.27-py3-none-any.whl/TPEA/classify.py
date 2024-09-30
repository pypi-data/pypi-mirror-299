#!/usr/bin/env python3
import os,sys,re
import collections
import argparse
import numpy as np
from Bio import SeqIO
from itertools import islice
import logging

def handle():
    return None

def deleteDuplicatedElement(listA):
    return sorted(set(listA), key = listA.index)

def progress_bar(finished_number,tasks_numbers):
    percentage=round(int(finished_number)/int(tasks_numbers)*100)
    print("\rDone "+format('['+str(finished_number)+'/'+str(tasks_numbers)+']')+" {}%: ".format(percentage),"▋" * (percentage // 2), end="")
    sys.stdout.flush()
    if int(finished_number)==int(tasks_numbers):
        print("\n")

def LOOPNT(n):
    n=str(n)
    out='R'
    if len(n)<10:
        m=10-len(n)
        while m>0:
           out=out+str("0")
           m=m-1
    out=out+str(n)
    return out 
    
def SRRHISAT(SRR,SILVA,CPU,miniLen):
    ###Step1
    cmd='fastq-dump --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 -M '+str(miniLen)+' --clip '+str(SRR)
    logging.info('Downloading reads for '+str(SRR)+" by fastq-dump\n")
    os.system(cmd)
    read1=str(SRR)+'_pass_1.fastq.gz'
    read2=str(SRR)+'_pass_2.fastq.gz'
    ###Step2
    HISATSUMMARY=str(SRR)+'.summary'
    HISATSAM=str(SRR)+'.sam'
    cmd='hisat2 -x '+str(SILVA)+' -1 '+str(read1)+' -2 '+str(read2)+' -p '+str(CPU)+' --summary-file '+str(HISATSUMMARY)+' --no-unal --no-hd -S '+str(HISATSAM)
    logging.info('Aligning reads against '+str(SILVA)+" by hisat2\n")
    os.system(cmd)
    #cmd="rm -f "+str(read1)+" "+str(read2)
    #os.system(cmd)
    
    cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
    os.system(cmd)
    #cmd="rm -f "+str(HISATSAM)
    #os.system(cmd)

def SRRHISATSIN(SRR,SILVA,CPU,miniLen):
    ###Step1
    cmd='fastq-dump --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 -M '+str(miniLen)+' --clip '+str(SRR)
    logging.info('Downloading reads for '+str(SRR)+" by fastq-dump\n")
    os.system(cmd)
    read1=str(SRR)+'_pass.fastq.gz'
    ###Step2
    HISATSUMMARY=str(SRR)+'.summary'
    HISATSAM=str(SRR)+'.sam'
    cmd='hisat2 -x '+str(SILVA)+' -U '+str(read1)+' -p '+str(CPU)+' --summary-file '+str(HISATSUMMARY)+' --no-unal --no-hd -S '+str(HISATSAM)
    logging.info('Aligning reads against '+str(SILVA)+" by hisat2\n")
    os.system(cmd)
    #cmd="rm -f "+str(read1)+" "+str(read2)
    #os.system(cmd)
    
    cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
    os.system(cmd)
    #cmd="rm -f "+str(HISATSAM)
    #os.system(cmd)


def HISATFA(SRR,SILVA,CPU):
    ###Step1
    read1=str(SRR)+'_1.fasta'
    read2=str(SRR)+'_2.fasta'
    if (os.path.exists(read1)== True) and (os.path.exists(read2)== True):
        read1=str(SRR)+'_1.fasta'
        read2=str(SRR)+'_2.fasta'  
        HISATSUMMARY=str(SRR)+'.summary'
        HISATSAM=str(SRR)+'.sam'
        cmd='hisat2 -x'+str(SILVA)+' -f -1 '+str(read1)+' -2 '+str(read2)+' -p '+str(CPU)+' --summary-file '+str(HISATSUMMARY)+' --no-unal --no-hd -S '+str(HISATSAM)
        logging.info('Aligning reads against '+str(SILVA)+" by hisat2\n")
        os.system(cmd)
        cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
        os.system(cmd)
    else:
        read1=str(SRR)+'_1.fastq.gz'
        read2=str(SRR)+'_2.fastq.gz'
        if (os.path.exists(read1)== True) and (os.path.exists(read2)== True):
            cmd1="gunzip "+read1
            os.system(cmd1)
            Infile1=str(SRR)+"_1.fastq"
            OUT=str(SRR)+"_1.fasta"
            fp = open(OUT, "w")
            recs = SeqIO.parse(Infile1,"fastq")
            for rec in recs:
                Seq = rec.seq
                ID=rec.description
                IDS=ID.strip().split()
                p=IDS[1].strip().split(":")[0]
                ID=IDS[0]+"."+str(p)
                out=">"+str(ID)+"\n"+str(Seq)
                print(out,file=fp)
            fp.close()
        
            cmd2="gunzip "+read2
            os.system(cmd2)
            Infile2=str(SRR)+"_2.fastq"
            OUT=str(SRR)+"_2.fasta"
            fp = open(OUT, "w")
            recs = SeqIO.parse(Infile2,"fastq")
            for rec in recs:
                Seq = rec.seq
                ID=rec.description
                IDS=ID.strip().split()
                p=IDS[1].strip().split(":")[0]
                ID=IDS[0]+"."+str(p)
                out=">"+str(ID)+"\n"+str(Seq)
                print(out,file=fp)
            fp.close()
        
            read1=str(SRR)+'_1.fasta'
            read2=str(SRR)+'_2.fasta'  
            HISATSUMMARY=str(SRR)+'.summary'
            HISATSAM=str(SRR)+'.sam'
            cmd='hisat2 -x'+str(SILVA)+' -f -1 '+str(read1)+' -2 '+str(read2)+' -p '+str(CPU)+' --summary-file '+str(HISATSUMMARY)+' --no-unal --no-hd -S '+str(HISATSAM)
            logging.info('Aligning reads against '+str(SILVA)+" by hisat2\n")
            os.system(cmd)
            cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
            os.system(cmd)
        else:
            print(read1,read2)
            logging.info('Please prepare '+str(read1)+" and "+str(read2)+"\n")


def HISATLOCAL(SRR,SILVA,CPU):
    ###Step1
    read1=str(SRR)+'_1.fastq.gz'
    read2=str(SRR)+'_2.fastq.gz'
    if (os.path.exists(read1)== True) and (os.path.exists(read2)== True):
        ###Step2
        HISATSUMMARY=str(SRR)+'.summary'
        HISATSAM=str(SRR)+'.sam'
        cmd='hisat2 -x '+str(SILVA)+' -1 '+str(read1)+' -2 '+str(read2)+' -p '+str(CPU)+' --summary-file '+str(HISATSUMMARY)+' --no-unal --no-hd -S '+str(HISATSAM)
        logging.info('Aligning reads against '+str(SILVA)+" by hisat2\n")
        os.system(cmd)
        cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
        os.system(cmd)
    else:
        print(read1,read2)
        logging.info('Please prepare '+str(read1)+" and "+str(read2)+"\n")

def SRRCLASS(SRR,TaxB,RefID):
    ###Step1
    HISATSAM=str(SRR)+'.sam'
    Genus={}
    with open(TaxB,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[2]
            if Tax=='family':
                IDS=ID.strip().split(";")
                gID=IDS[-2]
                fID=IDS[-3]
                if gID!='uncultured':
                    Genus[gID]=fID
    LINKG={}
    with open(RefID,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[1]
            Taxs=Tax.strip().split(";")
            if 'Chloroplast' in Tax:
                LINKG[ID]='Chloroplast'
            elif 'Mitochondria' in Tax:
                LINKG[ID]='Mitochondria'
            else:
                if len(Taxs)>2:
                    for i in range(-3,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
                if len(Taxs)==2:
                    for i in range(-2,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
    READS=[]
    REFS=[]
    NRC={}
    MAPS=[]
    X=-1
    Y=-1
    with open(HISATSAM,"r") as infile:
        for line in infile:
            gff=line.strip()
            ID=gff.strip().split("\t")[0]
            ID1=ID.strip().split(".")[0]
            ID2=ID.strip().split(".")[1]
            ID3=ID.strip().split(".")[2]
            ID12=str(ID1)+"."+str(ID2)
            if NRC.get(ID12)==None:
                X=X+1
                NRC[ID12]=X
                READS.append(ID12)
            
            REF=gff.strip().split("\t")[2]
            if NRC.get(REF)==None:
                Y=Y+1
                NRC[REF]=Y
                REFS.append(REF)
        
            AM=gff.strip().split("\t")[5]
            MAP=str(ID12)+"\t"+str(REF)+"\t"+str(AM)+"\t"+str(ID3)
            MAPS.append(MAP)

    Z=len(MAPS)
    print(X,Y,Z)
    ###Step4
    Y=Y+1
    X=X+1
    arrayXYZ=np.full((Y,X,6),'XXXXXXXXXXX.XXXXXXX.XXXXXX')
    MapNumber=0
    print(MapNumber)
    for MAP in MAPS:
        MapNumber=MapNumber+1
        progress_bar(MapNumber, Z)
        ID=MAP.strip().split("\t")[0]
        REF=MAP.strip().split("\t")[1]
        P=MAP.strip().split("\t")[-1]
        MS=MAP.strip().split("\t")[2]
        X=NRC[ID]
        Y=NRC[REF]
        if LINKG.get(REF)!=None:
            G=LINKG[REF]
            #print(REF,G)
            if int(P)==1:
                arrayXYZ[Y,X,0]=str(G)
                arrayXYZ[Y,X,2]=str(REF)
                arrayXYZ[Y,X,4]=str(ID)
            if int(P)==2:
                arrayXYZ[Y,X,1]=str(G)
                arrayXYZ[Y,X,3]=str(REF)
                arrayXYZ[Y,X,5]=str(ID)
    
    RDC=str(SRR)+'.read.class1'
    fp = open(RDC, "w")
    outfile="Read\tNum\tFamilies\tRefGenes"
    print(outfile,file=fp)
    print("\nstep4\n")
    FAMILIES=[]
    READN={}
    for x in range(0,X):
        progress_bar(x,X)
        Read=READS[x]
        GENUS=np.unique(arrayXYZ[:,x,0:1])
        GENES=np.unique(arrayXYZ[:,x,2:3])
        GLS=[]
        if 'Chloroplast' not in GENUS and 'Mitochondria' not in GENUS:
            for z in GENUS:
                if z!='XXXXXXXXXXX.XXXXXXX.XXXXXX':
                    GLS.append(z)
                    FAMILIES.append(z)
            FAMILIES=deleteDuplicatedElement(FAMILIES)
        if 'Chloroplast' not in GENES and 'Mitochondria' not in GENES:        
            REFG=[]
            for z in GENES:
                if z!='XXXXXXXXXXX.XXXXXXX.XXXXXX':
                    REFG.append(z)
    
        num=len(GLS)
        if int(num)>0:
            READN[Read]=int(num)
            out=str(Read)+"\t"+str(num)+"\t"+str(GLS)+"\t"+str(REFG)
            print(out,file=fp)
    fp.close()

    print("\nclass2\n")

    RDC=str(SRR)+'.read.class2'
    fp = open(RDC, "w")
    outfile="Family\tRefGenes\tNum\tReads"
    print(outfile,file=fp)
    R=len(FAMILIES)
    rnum=0
    for f in FAMILIES:
        rnum=int(rnum)+1
        progress_bar(rnum,R)
        UNR=[]
        GENES=[]
        for gene in REFS:
            if LINKG.get(gene)!=None and NRC.get(gene)!=None:
                Family=LINKG[gene]
                y=NRC[gene]
                tnum=0
                if f==Family:
                    READS=np.unique(arrayXYZ[y,:,4:5])
                    for r in READS:
                        if r!='XXXXXXXXXXX.XXXXXXX.XXXXXX' and READN.get(r)!=None:
                            RN=READN[r]
                            #print(RN)
                            if int(RN)==1:
                                UNR.append(r)
                                tnum=1
                if int(tnum)>0:
                    GENES.append(gene)
        UNRN=len(UNR)
        if int(UNRN)>0:
            out=str(f)+"\t"+str(GENES)+"\t"+str(UNRN)+"\t"+str(UNR)
            print(out,file=fp)
    fp.close()

    cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
    os.system(cmd)

def SAMC1FQ(SRR):
    READCLASS=str(SRR)+'.read.class1'
    MAPF={}
    MAPR={}
    with open(READCLASS,"r") as infile:
        for line in islice(infile, 1, None):
            ID=line.strip().split("\t")[0]
            ID1=ID+".1"
            MAPF[ID1]=1
            ID2=ID+".2"
            MAPR[ID2]=1
    read1=str(SRR)+'_sam_1.fq'
    read2=str(SRR)+'_sam_2.fq'
    fp1 = open(read1, "w")
    fp2 = open(read2, "w")
    HISATSAM=str(SRR)+'.sam'
    with open(HISATSAM,"r") as infile:
        for line in infile:
            ID=line.strip().split("\t")[0]
            RS=line.strip().split("\t")[9]
            RL=line.strip().split("\t")[10]
            if MAPF.get(ID)!=None:
                out="@"+ID+"\n"+RS+"\n"+"+\n"+RL
                print(out,file=fp1)
            if MAPR.get(ID)!=None:
                out="@"+ID+"\n"+RS+"\n"+"+\n"+RL
                print(out,file=fp2)
    fp1.close()
    fp2.close()

def MAPN(SRR,TaxB,RefID):
    ###Step1
    Genus={}
    with open(TaxB,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[2]
            if Tax=='family':
                IDS=ID.strip().split(";")
                gID=IDS[-2]
                fID=IDS[-3]
                if gID!='uncultured':
                    Genus[gID]=fID
    LINKG={}
    with open(RefID,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[1]
            Taxs=Tax.strip().split(";")
            if 'Chloroplast' in Tax:
                LINKG[ID]='Chloroplast'
            elif 'Mitochondria' in Tax:
                LINKG[ID]='Mitochondria'
            else:
                if len(Taxs)>2:
                    for i in range(-3,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
                if len(Taxs)==2:
                    for i in range(-2,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
    print(RefID)
    READS=[]
    REFS=[]
    NRC={}
    MAPS=[]
    X=-1
    Y=-1
    READIDN={}
    loopn=0
    HISATSAM=str(SRR)+'.sam'
    with open(HISATSAM,"r") as infile:
        for line in infile:
            gff=line.strip()
            ID=gff.strip().split("\t")[0]
            ID3=ID.strip().split(".")[-1]
            ID12=ID.strip().split(".")[0]
            if NRC.get(ID12)==None:
                loopn=loopn+1
                NewID=LOOPNT(loopn)
                READIDN[NewID]=ID12
                READIDN[ID12]=NewID
                X=X+1
                NRC[NewID]=X
                READS.append(NewID)
            else:
                NewID=READIDN[ID12]

            REF=gff.strip().split("\t")[2]
            if NRC.get(REF)==None:
                Y=Y+1
                NRC[REF]=Y
                REFS.append(REF)
            AM=gff.strip().split("\t")[5]
            MAP=str(NewID)+"\t"+str(REF)+"\t"+str(AM)+"\t"+str(ID3)
            MAPS.append(MAP)
    print(HISATSAM)
    Z=len(MAPS)
    print(X,Y,Z)
    ###Step4
    Y=Y+1
    X=X+1
    arrayXYZ=np.full((Y,X,6),'XXXXXXXXXXXXXXX')
    MapNumber=0
    print(MapNumber)
    for MAP in MAPS:
        MapNumber=MapNumber+1
        progress_bar(MapNumber, Z)
        ID=MAP.strip().split("\t")[0]
        REF=MAP.strip().split("\t")[1]
        P=MAP.strip().split("\t")[-1]
        MS=MAP.strip().split("\t")[2]
        X=NRC[ID]
        Y=NRC[REF]
        if LINKG.get(REF)!=None:
            G=LINKG[REF]
            #print(REF,G)
            if int(P)==1:
                arrayXYZ[Y,X,0]=str(G)
                arrayXYZ[Y,X,2]=str(REF)
                arrayXYZ[Y,X,4]=str(ID)
            if int(P)==2:
                arrayXYZ[Y,X,1]=str(G)
                arrayXYZ[Y,X,3]=str(REF)
                arrayXYZ[Y,X,5]=str(ID)
    
    RDC=str(SRR)+'.read.class1'
    fp = open(RDC, "w")
    outfile="Read\tNum\tFamilies\tRefGenes"
    print(outfile,file=fp)
    print("\nstep4\n")
    FAMILIES=[]
    READN={}
    for x in range(0,X):
        progress_bar(x,X)
        Read=READS[x]
        GENUS=np.unique(arrayXYZ[:,x,0:1])
        GENES=np.unique(arrayXYZ[:,x,2:3])
        GLS=[]
        if 'Chloroplast' not in GENUS and 'Mitochondria' not in GENUS:
            for z in GENUS:
                if z!='XXXXXXXXXXXXXXX':
                    GLS.append(z)
                    FAMILIES.append(z)
            FAMILIES=deleteDuplicatedElement(FAMILIES)
        if 'Chloroplast' not in GENES and 'Mitochondria' not in GENES:        
            REFG=[]
            for z in GENES:
                if z!='XXXXXXXXXXXXXXX':
                    REFG.append(z)
    
        num=len(GLS)
        if int(num)>0:
            READN[Read]=int(num)
            Rread=READIDN[Read]
            out=str(Rread)+"\t"+str(num)+"\t"+str(GLS)+"\t"+str(REFG)
            print(out,file=fp)
    fp.close()

    print("\nclass2\n")

    RDC=str(SRR)+'.read.class2'
    fp = open(RDC, "w")
    outfile="Family\tRefGenes\tNum\tReads"
    print(outfile,file=fp)
    R=len(FAMILIES)
    rnum=0
    for f in FAMILIES:
        rnum=int(rnum)+1
        progress_bar(rnum,R)
        UNR=[]
        GENES=[]
        for gene in REFS:
            if LINKG.get(gene)!=None and NRC.get(gene)!=None:
                Family=LINKG[gene]
                y=NRC[gene]
                tnum=0
                if f==Family:
                    READS=np.unique(arrayXYZ[y,:,4:5])
                    for r in READS:
                        if r!='XXXXXXXXXXXXXXX' and READN.get(r)!=None:
                            RN=READN[r]
                            #print(RN)
                            if int(RN)==1:
                                rRID=READIDN[r]
                                UNR.append(rRID)
                                tnum=1
                if int(tnum)>0:
                    GENES.append(gene)
        UNRN=len(UNR)
        if int(UNRN)>0:
            out=str(f)+"\t"+str(GENES)+"\t"+str(UNRN)+"\t"+str(UNR)
            print(out,file=fp)
    fp.close()
    READIDN={}
    cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
    os.system(cmd)


def SRRCLASSSIN(SRR,TaxB,RefID):
    ###Step1
    HISATSAM=str(SRR)+'.sam'
    Genus={}
    with open(TaxB,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[2]
            if Tax=='family':
                IDS=ID.strip().split(";")
                gID=IDS[-2]
                fID=IDS[-3]
                if gID!='uncultured':
                    Genus[gID]=fID
    LINKG={}
    with open(RefID,"r") as infile:
        for line in infile:
            tax=line.strip()
            ID=tax.strip().split("\t")[0]
            Tax=tax.strip().split("\t")[1]
            Taxs=Tax.strip().split(";")
            if 'Chloroplast' in Tax:
                LINKG[ID]='Chloroplast'
            elif 'Mitochondria' in Tax:
                LINKG[ID]='Mitochondria'
            else:
                if len(Taxs)>2:
                    for i in range(-3,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
                if len(Taxs)==2:
                    for i in range(-2,1,1):
                        R=Taxs[i]
                        if Genus.get(R)!=None:
                            LINKG[ID]=R
    READS=[]
    REFS=[]
    NRC={}
    MAPS=[]
    X=-1
    Y=-1
    with open(HISATSAM,"r") as infile:
        for line in infile:
            gff=line.strip()
            ID=gff.strip().split("\t")[0]
            ID1=ID.strip().split(".")[0]
            ID2=ID.strip().split(".")[1]
            ID3=ID.strip().split(".")[2]
            ID12=str(ID1)+"."+str(ID2)
            if NRC.get(ID12)==None:
                X=X+1
                NRC[ID12]=X
                READS.append(ID12)
            
            REF=gff.strip().split("\t")[2]
            if NRC.get(REF)==None:
                Y=Y+1
                NRC[REF]=Y
                REFS.append(REF)
        
            AM=gff.strip().split("\t")[5]
            MAP=str(ID12)+"\t"+str(REF)+"\t"+str(AM)
            MAPS.append(MAP)

    Z=len(MAPS)
    print(X,Y,Z)
    ###Step4
    Y=Y+1
    X=X+1
    arrayXYZ=np.full((Y,X,3),'XXXXXXXXXXX.XXXXXXX.XXXXXX')
    MapNumber=0
    print(MapNumber)
    for MAP in MAPS:
        MapNumber=MapNumber+1
        progress_bar(MapNumber, Z)
        ID=MAP.strip().split("\t")[0]
        REF=MAP.strip().split("\t")[1]
        MS=MAP.strip().split("\t")[2]
        X=NRC[ID]
        Y=NRC[REF]
        if LINKG.get(REF)!=None:
            G=LINKG[REF]
            #print(REF,G)
            arrayXYZ[Y,X,0]=str(G)
            arrayXYZ[Y,X,1]=str(REF)
            arrayXYZ[Y,X,2]=str(ID)
    
    RDC=str(SRR)+'.read.class1'
    fp = open(RDC, "w")
    outfile="Read\tNum\tFamilies\tRefGenes"
    print(outfile,file=fp)
    print("\nstep4\n")
    FAMILIES=[]
    READN={}
    for x in range(0,X):
        progress_bar(x,X)
        Read=READS[x]
        GENUS=np.unique(arrayXYZ[:,x,0])
        GENES=np.unique(arrayXYZ[:,x,1])
        GLS=[]
        if 'Chloroplast' not in GENUS and 'Mitochondria' not in GENUS:
            for z in GENUS:
                if z!='XXXXXXXXXXX.XXXXXXX.XXXXXX':
                    GLS.append(z)
                    FAMILIES.append(z)
            FAMILIES=deleteDuplicatedElement(FAMILIES)
        if 'Chloroplast' not in GENES and 'Mitochondria' not in GENES:        
            REFG=[]
            for z in GENES:
                if z!='XXXXXXXXXXX.XXXXXXX.XXXXXX':
                    REFG.append(z)
    
        num=len(GLS)
        if int(num)>0:
            READN[Read]=int(num)
            out=str(Read)+"\t"+str(num)+"\t"+str(GLS)+"\t"+str(REFG)
            print(out,file=fp)
    fp.close()

    print("\nclass2\n")

    RDC=str(SRR)+'.read.class2'
    fp = open(RDC, "w")
    outfile="Family\tRefGenes\tNum\tReads"
    print(outfile,file=fp)
    R=len(FAMILIES)
    rnum=0
    for f in FAMILIES:
        rnum=int(rnum)+1
        progress_bar(rnum,R)
        UNR=[]
        GENES=[]
        for gene in REFS:
            if LINKG.get(gene)!=None and NRC.get(gene)!=None:
                Family=LINKG[gene]
                y=NRC[gene]
                tnum=0
                if f==Family:
                    READS=np.unique(arrayXYZ[y,:,2])
                    for r in READS:
                        if r!='XXXXXXXXXXX.XXXXXXX.XXXXXX' and READN.get(r)!=None:
                            RN=READN[r]
                            #print(RN)
                            if int(RN)==1:
                                UNR.append(r)
                                tnum=1
                if int(tnum)>0:
                    GENES.append(gene)
        UNRN=len(UNR)
        if int(UNRN)>0:
            out=str(f)+"\t"+str(GENES)+"\t"+str(UNRN)+"\t"+str(UNR)
            print(out,file=fp)
    fp.close()

    cmd="tar -czvf "+str(HISATSAM)+".tgz "+str(HISATSAM)
    os.system(cmd)