import os
import Bio
import numpy as np
import pandas as pd
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastnCommandline


parser = argparse.ArgumentParser(description="""Main script of PhaSUIT.""")
parser.add_argument('--bfile', help='FASTA file of bacterial contigs',  default = 'NONE')
parser.add_argument('--bfolder', help='Folder of the bacterial contigs',  default = 'NONE')
parser.add_argument('--pfile', help='FASTA file of phage contigs',  default = 'inputs.fa')
parser.add_argument('--ident', help='ident threshold for the alignment',  default = 75)
parser.add_argument('--threads', help='number of threads to use', type=int, default=8)
parser.add_argument('--rootpth', help='rootpth of the user', default='user_0/')
parser.add_argument('--out', help='output path of the user', default='out/')
parser.add_argument('--midfolder', help='mid folder for intermidiate files', default='midfolder/')
parser.add_argument('--dbdir', help='database directory',  default = 'database/')
inputs = parser.parse_args()



threads   = inputs.threads
bfile     = inputs.bfile
bfolder   = inputs.bfolder
pfile     = inputs.pfile
rootpth   = inputs.rootpth
out       = inputs.out
dbdir     = inputs.dbdir
midfolder = inputs.midfolder
evalue    = inputs.ident

if not os.path.exists(rootpth):
    os.system(f'mkdir {rootpth}')
    os.system(f'mkdir {rootpth}/{out}')
    os.system(f'mkdir {rootpth}/{midfolder}')


######################################################
#################  single file  ######################
######################################################
# running CRT
if bfolder == 'NONE':
    pos2name={}
    cur = 0
    seq = ''
    comb_name = bfile.split('/')[-1]
    comb_name = comb_name.rsplit('.')[0]
    with open(f'{rootpth}/{midfolder}/{comb_name}_comb.fa', 'w') as file:
        _=file.write('>Seq\n')
        for record in SeqIO.parse(f'{bfile}', 'fasta'):
            pos2name[cur] = record.id
            _=file.write(f'{str(record.seq)}----------\n')
            cur += len(record.seq) + 10

    outputfile = comb_name + '.crispr'

    os.system(f'java -cp {dbdir}/CRT1.2-CLI.jar crt {rootpth}/{midfolder}/{comb_name}_comb.fa {rootpth}/{midfolder}/{outputfile}')

    # Parser for CRT
    crispr_rec = []
    pos_list = list(pos2name.keys())
    old_accession = pos2name[0]
    cnt = 0
    cur = 0
    with open(f'{rootpth}/{midfolder}/{outputfile}') as file_in:
        for line in file_in:
            tmp_list = line.split("\t")
            try:
                pos = int(tmp_list[0])
            except:
                continue
            # find accession
            start = cur
            for i in range(start, len(pos_list)):
                if pos > pos_list[i+1]:
                    continue
                else:
                    cur = i
                    accession = pos2name[pos_list[i]]
                    if old_accession == accession:
                        cnt += 1
                    else:
                        old_accession = accession
                        cnt = 0
                    break
            if tmp_list[3] == '\n':
                continue
            rec = SeqRecord(Seq(tmp_list[3]), id=f'{old_accession}_CRISPR_{cnt}', description='')
            cnt += 1
            crispr_rec.append(rec)
            #except:
            #    continue
                    
    if crispr_rec:
        SeqIO.write(crispr_rec, f"{rootpth}/{midfolder}/CRISPRs.fa", 'fasta')
    else:
        print('No CRISPRs found in the contigs.')
        exit(0)
    
######################################################
#################  folder file  ######################
######################################################
elif bfile == 'NONE':
    os.system(f'mkdir {rootpth}/{midfolder}/crispr_tmp')
    os.system(f'mkdir {rootpth}/{midfolder}/crispr_fa')
    for bfile in os.listdir(f'{bfolder}'):
        prefix = bfile.rsplit('.', 1)[0]
        outputfile = prefix + '.crispr'

        os.system(f'java -cp {dbdir}/CRT1.2-CLI.jar crt {bfolder}/{bfile} {rootpth}/{midfolder}/crispr_tmp/{outputfile}')

        crispr_rec = []
        with open(f'{rootpth}/{midfolder}/crispr_tmp/{outputfile}') as file_in:
            for line in file_in:
                if line.startswith('ORGANISM:'):
                    accession = line.split(' ')[2]
                    cnt = 0
                else:
                    tmp_list = line.split("\t")
                    try:
                        _ = int(tmp_list[0])
                        if tmp_list[3] == '\n':
                            continue
                        rec = SeqRecord(Seq(tmp_list[3]), id=f'{prefix}_CRISPR_{cnt}', description='')
                        cnt += 1
                        crispr_rec.append(rec)
                    except:
                        continue
                        
        if crispr_rec:
            SeqIO.write(crispr_rec, f"{rootpth}/{midfolder}/crispr_fa/{prefix}_CRISPRs.fa", 'fasta')

    rec = []
    for file in os.listdir(f'{rootpth}/{midfolder}/crispr_fa/'):
        for record in SeqIO.parse(f'{rootpth}/{midfolder}/crispr_fa/{file}', 'fasta'):
            rec.append(record)
    if rec:
        SeqIO.write(rec, f"{rootpth}/{midfolder}/CRISPRs.fa", 'fasta')
    else:
        print('No CRISPRs found in the contigs.')
        exit(0)

else:
    print("Parameters Error!")
    exit(0)




# construct database and run blast
os.system(f'mkdir {rootpth}/{midfolder}/crispr_db')
os.system(f'makeblastdb -in {rootpth}/{midfolder}/CRISPRs.fa -dbtype nucl -parse_seqids -out {rootpth}/{midfolder}/crispr_db/allCRISPRs')


query_file = pfile
db_host_crispr_prefix = f"{rootpth}/{midfolder}/crispr_db/allCRISPRs"
output_file = f"{rootpth}/{midfolder}/crispr_pred.tab"
crispr_call = NcbiblastnCommandline(query=query_file,db=db_host_crispr_prefix,out=output_file,outfmt="6 qseqid sseqid evalue pident length slen", evalue=1,gapopen=10,penalty=-1,
                                  gapextend=2,word_size=7,dust='no',
                                 task='blastn-short',perc_identity=90,num_threads=threads)
crispr_call()


# parse the BLASTN result
Accession = []
prediction = []
with open(output_file) as file_out:
    for line in file_out.readlines():
        parse = line.replace("\n", "").split("\t")
        virus = parse[0]
        prokaryote = parse[1]
        ident = float(parse[-3])
        length = float(parse[-2])
        slen = float(parse[-1])
        if ident > evalue:
            Accession.append(virus)
            prediction.append(prokaryote.split('_CRISPR_')[0])

df = pd.DataFrame({"phage_contig": Accession, "bacteria_contig": prediction})
df = df.drop_duplicates()

df.to_csv(f'{rootpth}/{out}/cherry_lite_pred.csv', index=False)
