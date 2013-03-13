import pandas as pd
import os

os.chdir('/miseqdata/Annotation_files')
xls = pd.ExcelFile('52GenesWithExonCoordinates-EDIT-2-28-13.xlsx')
bedDF = xls.parse('52GeneLib',header=None,parse_cols=5)
bedDF.groupby(0)
GroupedByGeneSymbol = []
for x,y in bedDF.groupby(0):
    print type(y)
    print x
    GroupedByGeneSymbol.append(y)
for group in GroupedByGeneSymbol:
    if group.irow(0)[5] == "-":
    #This numbers negative strand exons            
        group[6] = range((len(group)),0,-1)
    else:
    #This numbers positive stand exons
        group[6] = range(1,len(group)+1,1)
FixedBed = []
for group in GroupedByGeneSymbol:
    group[4] = group[6]
    FixedBed.append(group.drop(6,axis=1))
DFToWrite = pd.concat(FixedBed)
DFToWrite.to_csv('52GeneBedFile0228EDITS_ForDepthOfCoverage.bed',sep="\t", index=False,header = False,float_format = "%i")
DFToWrite.ix[1,[1,2,3,0,4,5]].to_csv('52GeneBedFile0228EDITS.bed',sep=" ", index=False,header = False,float_format = "%i")