import os,fnmatch,shutil,subprocess

class PrepareFiles():
    
    
    def __init__(self,RunDir):
        self.FilesToProcess = []   
        self.RunDir = RunDir
    def MakeDirs(self):
        for FastqFile in self.FilesToProcess: 
            SN = FastqFile[:FastqFile.find("-")]
            SN = os.path.join(self.RunDir,SN)
            os.makedirs(SN)
    def MoveFiles(self):
        a = [i for i in os.listdir(self.RunDir) if fnmatch.fnmatch(i,"*.gz") and not fnmatch.fnmatch(i,"Undet*")]
        for FastqFile in a:
            shutil.move(os.path.join(self.RunDir, FastqFile), os.path.join(self.RunDir, FastqFile[:FastqFile.find("-")]))
            A = "gunzip "+os.path.join(self.RunDir, FastqFile[:FastqFile.find("-")])+"/*.gz"
            subprocess.call(A ,shell=True)
    def GetNamesForDirs(self):
        self.FilesToProcess = [i for i in os.listdir(self.RunDir) if fnmatch.fnmatch(i,"*R1*.gz") and not fnmatch.fnmatch(i,"Undet*")]
    def __str__(self):
        return  " ".join(self.FilesToProcess)
    

def main():
    ProcessStuff = PrepareFiles("/miseqdata/130531_M00386_0023_000000000-A416J/Data/Intensities/BaseCalls/")
    ProcessStuff.GetNamesForDirs()
    print ProcessStuff
    ProcessStuff.MakeDirs()
    ProcessStuff.MoveFiles()

if __name__ == "__main__": main() 

