from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen 
import magic

if __name__ == '__main__':
   
    
    myFileToAnalyze="../Music/06 What You Know About Richard D. James.mp3";

    # need try catch
    openFile=mutagen.File(myFileToAnalyze)
    if (openFile != None):
              
        #define type of file
        #MyFileSplit=myFileToAnalyze.split('.')
        #extFile=""+MyFileSplit.__getitem__(MyFileSplit.__len__()-1)
        #extFile=extFile.lower()
        mime = magic.Magic(mime=True)
        typeMime=mime.from_file(myFileToAnalyze).split('/')[-1]
        print(typeMime)
        
        if (typeMime=='mpeg'):
            
            print(True)
            audio = MP3(myFileToAnalyze, ID3=EasyID3)
            print(audio)       
            
            print(audio.keys())
    else :
        print("FILE impossible to read by mutagen")
    pass