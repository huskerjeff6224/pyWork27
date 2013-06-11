import subprocess,glob
myfiles = glob.glob("*PANEL*")

for f in myfiles:
    subprocess.Popen('bgzip '+f,shell=True)

myfiles = glob.glob("*.gz")
for f in myfiles:
    subprocess.Popen('tabix -p vcf '+f,shell=True)

vcfstring = "/miseqdata/tools/vcftools_0.1.10/bin/vcf-merge " +" ".join(myfiles)
vcfstring = vcfstring + " > merged.vcf"
subprocess.Popen(vcfstring,shell=True)

subprocess.Popen('bgzip merged.vcf',shell=True)
subprocess.Popen(''tabix -p vcf merged.vcf',shell=True)
LOVDfile = glob.glob("../*LOVD*")

vcfstring = "/miseqdata/tools/vcftools_0.1.10/bin/vcf-isec -f -c merged.vcf "
vcfstring = vcfstring + str(LOVDfile[0]) + " > diff.vcf"
subprocess.Popen(vcfstring,shell=True)
