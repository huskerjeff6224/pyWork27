import pandas as pd
import os,sys,fnmatch,csv,glob,tarfile
import zipfile

def ParseCSV(FileToParse):
#Annovar will print data in data columns beyond(right) of the csv, this causes Panda to
#error because it does want columns beyond the column headers
#This function just drops all the data beyond the column headers (its not needed anyways)    
    with open(FileToParse,'r') as f:
        file=[]
        reader = csv.reader(f,dialect='excel')
        header = reader.next()
        #print len(header)
        for row in reader:
            file.append(row[:len(header)])
    return pd.DataFrame(file,columns=header)

def CreateExcel(FilesToMerge):
    ExcelWBWriter = pd.ExcelWriter(os.curdir+"/Variants.xlsx")
    for file in FilesToMerge:
        print file
        dfTemp = ParseCSV(os.curdir+"/"+file)
        #To find end position skip the extension "." then goto next one search backward
        #Sheet name can not exceed 31 characters
        EndPosition = file[:-4].rfind(".")
        
        StartPosition = (file.find("."))+1
        dfTemp = dfTemp[["Func","Gene","Chr","Start","End","Ref","Obs","Otherinfo","ExonicFunc",
        "AAChange","Conserved","SegDup","ESP6500_ALL",
        "1000g2012apr_ALL","dbSNP137","AVSIFT","LJB_PhyloP","LJB_PhyloP_Pred","LJB_SIFT",
        "LJB_SIFT_Pred","LJB_PolyPhen2","LJB_PolyPhen2_Pred","LJB_LRT","LJB_LRT_Pred",
        "LJB_MutationTaster","LJB_MutationTaster_Pred","LJB_GERP++"]]
        dfTemp.to_excel(ExcelWBWriter, file[StartPosition:EndPosition],index=False)
               
    ExcelWBWriter.save()
def FindGenomeSummaryFiles():
    return [file for file in os.listdir(os.curdir) if fnmatch.fnmatch(file, "*genome_summary*.csv") ]

def DeleteFiles(ListToDelete):
    for file in ListToDelete:
        os.remove(file)
        
def ZipFiles(ListToZip,SampleName):
    tar = tarfile.open(SampleName+".tar.bz2", "w:bz2")
    for name in ListToZip:
        tar.add(name)
    tar.close()        
    #No delete the files added to the tar
    DeleteFiles(ListToZip)
def CleanUpFiles():
    FilteredToDelete = glob.glob("*filtered")
    DeleteFiles(FilteredToDelete)
    BamFilesToDelete = [file for file in glob.glob("*.bam") if not fnmatch.fnmatch(file,"*recalibrated*")]
    DeleteFiles(BamFilesToDelete)
    BamIdxFilesToDelete = [file for file in glob.glob("*.bai") if not fnmatch.fnmatch(file,"*recalibrated*")]
    DeleteFiles(BamIdxFilesToDelete)
    IdxFilesToDelete = glob.glob("*.idx")
    DeleteFiles(IdxFilesToDelete)
    ExomeSummary = glob.glob("*exome_summary*")
    DeleteFiles(ExomeSummary)
    txtFilesToDelete = glob.glob("*input.txt")
    DeleteFiles(txtFilesToDelete)
    SaiFilesToDelete = glob.glob("*.sai")
    DeleteFiles(SaiFilesToDelete)
    logFilesToDelete = glob.glob("*.log")
    DeleteFiles(logFilesToDelete)
    FilesToKeepOutOfZip = ['.bam',".bai",".xlsx",".fastq",".bz2"]
    RestOfFiles = glob.glob("*")
    SampleName = "".join(glob.glob("*recalibrated.bam"))
    SampleName = SampleName[:SampleName.find(".")]
    ZipRestOfFiles=[]
    for file in  RestOfFiles:
        filename,ext = os.path.splitext(file)
        if ext not in FilesToKeepOutOfZip:
            ZipRestOfFiles.append(file)
    ZipFiles(ZipRestOfFiles,SampleName)       
        
    
print len(sys.argv)
if len(sys.argv)< 2:
    print "Need file path"
    exit()

os.chdir(sys.argv[1])
FilesToMerge = FindGenomeSummaryFiles()
print FilesToMerge
CreateExcel(FilesToMerge)
CleanUpFiles()

