import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from ToolBox.model import *
from _overlapped import NULL
 
if __name__ == '__main__':
   
    
    myFileToAnalyze="../Music/Swelling_-_05_-_Night_III.mp3";
  
    # need try catch
    openFile=mutagen.File(myFileToAnalyze)
    if (openFile != NULL):
       
        openFile.__format__().pprint()
        trestag=mutagen.Tags()
       
        
        MyFileSplit=myFileToAnalyze.split('.')
        extFile=""+MyFileSplit.__getitem__(MyFileSplit.__len__()-1)
        extFile=extFile.lower()
        if (extFile=='mp3'):
            print(True)
            audio = MP3(myFileToAnalyze, ID3=EasyID3)
            print(audio)       
            print(audio.keys())
    else :
        print("FILE impossible to read by mutagen")
    pass