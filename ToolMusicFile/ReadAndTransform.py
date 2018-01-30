import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen 
#import magic
from ToolMusicFile.ModelTrack import ModelTrack


def DefineMetadataFromMime(mutagenFile):
    ''' define metadata , depending of Mime Type'''
    dictionnaryMetadata={}
    typeMime=mutagenFile.mime    
    # CASE MP3
    if ('audio/mp3' in typeMime):
        try :
            dictionnaryMetadata=MP3(myFileToAnalyze, ID3=EasyID3)
        except :
            print("problem to case MP3") 
    # CASE FLAC
    # CASE OGG
    else :
        print("Mime file not taken")
    return dictionnaryMetadata;

def ReadTrackFileAndTransform(pathToTrack):
    myFileName=pathToTrack.split('/')[-1]
    
    openFile=mutagen.File(pathToTrack)
    if (openFile != None): 
        typeMime=openFile.mime
        dictioMetadata=DefineMetadataFromMime(openFile)
        track=ModelTrack(myFileName,dictioMetadata,typeMime)
        return track
    else :
        print("FILE impossible to read by mutagen")


if __name__ == '__main__':
    os.chdir("../music/")
    
    myFileToAnalyze="06 What You Know About Richard D. James.mp3";
    
    myTrack=ReadTrackFileAndTransform(myFileToAnalyze)
    
    print(myTrack.dicAttTrack)

    pass