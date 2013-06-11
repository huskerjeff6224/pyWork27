import os,subprocess,fnmatch,re
os.chdir("/miseqdata/ALS_PROJECT")
RefGenome = "/miseqdata/safer/genomes/Homo_sapiens/UCSC/hg19/Sequence/WholeGenomeFasta/ucsc.hg19.fasta "

for folder in os.listdir(os.curdir):
    if os.path.isdir(folder):
       fastqfiles = [ file for file in os.listdir(os.curdir+"/"+folder) if fnmatch.fnmatch("*.fastq",file)] 
       fastqfiles.sort()
       
       for fastqfile in fastqfiles:
           ReadNum = re.search("?P<ReadNum>(R?)",fastqfile)
           AlnCmd ='bwa aln -1 -t 10 ' +RefGenome + ReadNum.group('ReadNum') + ".sai" 
           subprocess.Popen(AlnCmd, shell=True)
    
       alignmentCmd =  "bwa sampe -A -P -r '@RG\tID:"+ folder+"\tPL:ILLUMINA' " +RefGenome+ fastqfiles[0]+ " " \
       + fastqfiles[1] + "R1.sai R2.sai > " + folder + ".sam"
       subprocess.Popen(alignmentCmd, shell=True)
       
       
#bwa aln -1 -t 8 GRCh37.p5.bwaRef mate1.trimmed.fastq mate1.sai
#bwa aln -2 -t 8 GRCh37.p5.bwaRef mate2.trimmed.fastq mate2.sai
#bwa sampe -A -P -r “@RG\tID:sample\tPL:ILLUMINA” GRCh37.p5.bwaRef mate1 mate2.sai mate1.trimmed.fastq mate2.trimmed.fastq > sample.sam
#samtools mpileup -A -d 1000000 -q 0 -Q 0 -f GRCh37.p5.fasta \
#sample.bam > sample.pileup;