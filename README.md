# CHERRY-crispr version


CHERRY is a python library for predicting the interactions between viral and prokaryotic genomes. CHERRY is based on a deep learning model, which consists of a graph convolutional encoder and a link prediction decoder.


In this program, we provide a simplified version of CHERRY, which only used the CRISPRs information in CHERRY's graph for host prediction. In addition, in this lite version, we provide a more easier way to predict the links between bacterial contigs and phage contigs. The sketch of CHERRY-crispr is shown as below:


```

Input (provided by user):
    1. bacterial contigs from their samples (FASTA files)
    2. phage contigs from their samples (FASTA files)

Output:
    The links (interactions) between bacteria and phages (CSV files)
```


## Required Dependencies

* Python 3.x
* Pandas
* Numpy
* Biopython
* NCBI BLAST+

## An easiler way to install

**Note**: If you have already install phabox env, you can skip this part

We suggest you install all the packages using conda (both Miniconda and Anaconda are ok) following the command lines below:

```
conda create --name cherry_crispr python=3.8
conda activate cherry_crispr

conda install pandas numpy biopython

conda install blast -c bioconda
```

## Usage

Once install the required environments, you need to activate it when you want to use:

```
conda activate cherry_crispr
```

Then, the commond of CHERRY-crispr can be called by:


```
python PATH_TO_CHERRY_CRISPR/cherry_crispr.py --bfolder PATH_TO_BACTERIA --pfile PATH_TO_PHAGE --ident IDENTITY_THRESHOLD --threads NUM_OF_THREAD --rootpth PATH_TO_OUTPUT --dbdir PATH_TO_CHERRY_CRISPR/database

OR

python PATH_TO_CHERRY_CRISPR/cherry_crispr.py --bfile PATH_TO_BACTERIA --pfile PATH_TO_PHAGE --ident IDENTITY_THRESHOLD --threads NUM_OF_THREAD --rootpth PATH_TO_OUTPUT --dbdir PATH_TO_CHERRY_CRISPR/database

```

There are two options for bacterial contigs:

1. --bfolder: the folder where you store your bacterial contigs (all the contigs should be FASTA files)

2. --bfile: the file where you store your bacterial contigs (FASTA file)


For example:

```
python CHERRY_crispr/cherry_crispr.py --bfolder ~/bacteria/ --pfile ~/phage.fa --threads 40 --rootpth ~/test_dir --dbdir CHERRY_crispr/database

OR

python CHERRY_crispr/cherry_crispr.py --bfile ~/bacteria.fa --pfile ~/phage.fa --threads 40 --rootpth ~/test_dir --dbdir CHERRY_crispr/database

```

## Outputs

There are three output files in `--rootpth PATH_TO_OUTPUT`.

1. CRISPRs.fa: CRISPRs found in your provided bacteria FASTA
2. crispr_align.txt: BLASTN results between CRISPR and phage
3. cherry_crispr_pred.csv: CSV files of the prediction (alignment > `--ident IDENTITY_THRESHOLD`)



## Citation
If you use this program, please cite the following papers:

* CHERRY:
```
Jiayu Shang, Yanni Sun, CHERRY: a Computational metHod for accuratE pRediction of virus–pRokarYotic interactions using a graph encoder–decoder model, Briefings in Bioinformatics, 2022;, bbac182, https://doi.org/10.1093/bib/bbac182
```

* CRT:
```
Bland C, Ramsey TL, Sabree F, Lowe M, Brown K, Kyrpides NC, Hugenholtz P:
CRISPR Recognition Tool (CRT): a tool for automatic detection of clustered regularly interspaced palindromic repeats. BMC Bioinformatics. 2007 Jun 18;8(1):209
```

The original version of CHERRY can be found via: [CHERRY](https://github.com/KennthShang/CHERRY)

