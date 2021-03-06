from __future__ import print_function
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
        if file == []:
            blankstring = []
            for i in xrange(0,len(header)):
                blankstring.append(" ")
            file.append(blankstring)
    return pd.DataFrame(file,columns=header)


def ConcatDFGroups(dataframe):
    #need to make a empty dataframe row to seperate groups
    if dataframe.ix[0,0] == " ":
        return dataframe
    ColNames = ["Func", "Gene", "ExonicFunc", "AAChange", "Conserved", "SegDup", "ESP6500_ALL",
                "1000g2012apr_ALL", "dbSNP137", "AVSIFT", "LJB_PhyloP", "LJB_PhyloP_Pred", 
                "LJB_SIFT", "LJB_SIFT_Pred", "LJB_PolyPhen2", "LJB_PolyPhen2_Pred", "LJB_LRT",
                "LJB_LRT_Pred", "LJB_MutationTaster", "LJB_MutationTaster_Pred", "LJB_GERP++",
                "Chr", "Start", "End", "Ref", "Obs", "Otherinfo"]
    EmptyData=[]
    #To create rows the you have make a list a list otherwise its just a single column
    EmptyData.append(list(" "*27))
    EmptyDF = pd.DataFrame(EmptyData,columns=ColNames)
    #create dictionary of dataframe groups by mutation type
    DictOfGroups = {i:h for (i,h) in dataframe.groupby(['Func'])}
    OrderOfMutationType = ['exonic','exonic;splicing', 'splicing', 'UTR5', 'ncRNA_exonic', 'intronic', 'UTR3', 'upstream']
    #This will concat empty space between lines
    dfTemp=1
    for MutType in OrderOfMutationType:
        if DictOfGroups.has_key(MutType):
            if isinstance(dfTemp,int):
                if MutType == 'exonic':
                    dfTemp = DictOfGroups[MutType].sort_index(by="ExonicFunc")
                    del DictOfGroups[MutType]
                else:
                    dfTemp = DictOfGroups[MutType]
                    del DictOfGroups[MutType]
            else:   
                dfTemp = pd.concat([dfTemp,EmptyDF,DictOfGroups[MutType]])
                del DictOfGroups[MutType]
    for key in DictOfGroups.keys():
        dfTemp = pd.concat([dfTemp,DictOfGroups[key]])
    
    return dfTemp            
#def ParseAAChangeColumn(dfTemp):
    #create new dataframe with AA split, then merge it back with orginal data
    #pass
    #dfTemp.AAChange
              
def CreateExcel(FilesToMerge):
    ExcelWBWriter = pd.ExcelWriter(os.curdir+"/Variants.xlsx")
    for file in FilesToMerge:
        print(file)
        dfTemp = ParseCSV(os.curdir+"/"+file)
        #dfTemp = ParseAAChangeColumn(dfTemp)
        #To find end position skip the extension "." then goto next one search backward
        #Sheet name can not exceed 31 characters
        EndPosition = file[:-4].rfind(".")
        
        StartPosition = (file.find("."))+1
        
        #Need to group by variant function
        dfTemp = ConcatDFGroups(dfTemp)
        
        #reorder file -- could have done this in the dfTemp.to_excel  
        dfTemp = dfTemp[["Func","Gene","Chr","Start","End","Ref","Obs",
                         "Otherinfo","ExonicFunc",
        "AAChange","Conserved","SegDup","ESP6500_ALL",
        "1000g2012apr_ALL","dbSNP137","AVSIFT","LJB_PhyloP","LJB_PhyloP_Pred","LJB_SIFT",
        "LJB_SIFT_Pred","LJB_PolyPhen2","LJB_PolyPhen2_Pred","LJB_LRT","LJB_LRT_Pred",
        "LJB_MutationTaster","LJB_MutationTaster_Pred","LJB_GERP++"]]
        #This saves the tabs
        dfTemp.to_excel(ExcelWBWriter, file[StartPosition:EndPosition],index=False)
        #dfTemp.to_csv(file[StartPosition:EndPosition]+".csv")
    #Write the workbook           
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
    MpileupFilesToDelete = glob.glob("*.mpileup")
    DeleteFiles(MpileupFilesToDelete)
    SamFilesToDelete = glob.glob("*.sam")
    DeleteFiles(SamFilesToDelete)
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
        if ext not in FilesToKeepOutOfZip and not fnmatch.fnmatch(file, "*LOVD*.vcf"):
            ZipRestOfFiles.append(file)
    ZipFiles(ZipRestOfFiles,SampleName)       
        
    
print(len(sys.argv))
if len(sys.argv)< 2:
    print("Need file path")
    exit()

os.chdir(sys.argv[1])
FilesToMerge = FindGenomeSummaryFiles()
print(FilesToMerge)
CreateExcel(FilesToMerge)
CleanUpFiles()

