# Files are generated from HISAT2 alignment.

##### SAMTOOLS #####

#!/bin/bash
#PBS -N SAM_TO_BAM
#PBS -l select=1:ncpus=16:mem=64gb,walltime=05:59:00
#PBS -j oe
#PBS -m ae
#PBS -M zID@unsw.edu.au
#PBS -J 0-526

PARAMS=(SCZD+CNTRL)

cd /srv/scratch/DIR/HISAT2_aln
module load samtools/1.20
samtools sort -@ 8 -O BAM -o ./${PARAMS[$PBS_ARRAY_INDEX]}.bam ./hisat_${PARAMS[$PBS_ARRAY_INDEX]}.sam
# both outputs remain (sam and bam)

################################################

### STRINGTIE assembly ###

#!/bin/bash
#PBS -N STRINGTIE_A
#PBS -l select=1:ncpus=16:mem=128gb,walltime=11:59:00
#PBS -j oe
#PBS -m ae
#PBS -M zID@unsw.edu.au
#PBS -J 0-526

cd /srv/scratch/DIR/HISAT2_aln

module load stringtie/1.3.4d

stringtie -p 8 -G /srv/scratch/DIR/gencode.v49.annotation.gtf -o /srv/scratch/DIR/STRINGTIE_A/${PARAMS[$PBS_ARRAY_INDEX]}.gtf ./${PARAMS[$PBS_ARRAY_INDEX]}.bam 


### STRINGTIE merge ###

#!/bin/bash
#PBS -N STRINGTIE_merge
#PBS -l select=1:ncpus=16:mem=128gb,walltime=11:59:00
#PBS -j oe
#PBS -m ae
#PBS -M zID@unsw.edu.au

cd /srv/scratch/DIR/STRI_merge

module load stringtie/1.3.4d

stringtie --merge -p 8 -G /srv/scratch/DIR/gencode.v49.annotation.gtf -o ST_merged.gtf mergedlist.txt


### STRINGTIE eB ###
#!/bin/bash
#PBS -N STRINGTIE_eB2
#PBS -l select=1:ncpus=16:mem=128gb,walltime=11:59:00
#PBS -j oe
#PBS -m ae
#PBS -M zID@unsw.edu.au
#PBS -J 0-526

PARAMS=(SCZD+CNTRL)

cd /srv/scratch/DIR/HISAT2_aln

module load stringtie/1.3.4d

stringtie -e -B -p 8 -G /srv/scratch/DIR/STRI_merge/ST_merged.gtf -o /srv/scratch/DIR/STRINGTIE_eB2/${PARAMS[$PBS_ARRAY_INDEX]}.gtf ./${PARAMS[$PBS_ARRAY_INDEX]}.bam -A gene_abund.tab

################################################

##### prepDE.py3 #####
# due to the number of files and to prevent errors, also sent as a PBS script - but not necessary with smaller datasets
# STRINGTIE_eB_list.txt is a text file with all the parameters listed to be fed into the script. 

#!/bin/bash
#PBS -N prepDE.py3_job
#PBS -l select=1:ncpus=16:mem=128gb,walltime=11:59:00
#PBS -j oe
#PBS -m ae
#PBS -M zID@unsw.edu.au

cd /srv/scratch/DIR/

python3 /srv/scratch/DIR/prepDE.py3 -i /srv/scratch/DIR/STRINGTIE_eB2/STRINGTIE_eB_list.txt -g /srv/scratch/DIR/STRINGTIE_eB2/gene_count_matrix.csv -t /srv/scratch/DIR/STRINGTIE_eB2/transcript_count_matrix.csv -l 100
