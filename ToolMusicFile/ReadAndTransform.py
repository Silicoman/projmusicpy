import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen 
#import magic
from ToolMusicFile.ModelTrack import ModelTrack
import logging
from pymongo import *
import sys
import gridfs

def DefineMetadataFromMime(myFile):
    ''' define metadata/tags of audio file put value in a dict,
        operation depending of Mime Type'''
    
    dictionaryMetadata={}
    typeMime=mutagen.File(myFile).mime    
    
    # CASE MP3
    if ('audio/mp3' in typeMime):
        try :
            tags=EasyID3(myFile)
            for i in tags. keys():
                dictionaryMetadata[i]=tags.get(i)[0] # 0 because tagValue is a list, takes directly the first value
            logging.info('From DefineMetadataFromMime: good extraction tags from the file: '+myFile)
            return dictionaryMetadata;
        except :
            print("problem to case MP3")
            logging.error('From DefineMetadataFromMime: error extraction tags from the file: '+myFile)
    # CASE FLAC
    # CASE OGG
    else :
        logging.error("Your file "+ myFile + " has a Mime file not taken")
    # if has not return a dico:
    return None

def ReadTrackFileAndTransform(pathToTrack):
    ''' Read a music file and transform it in a standard object'''
    myFileName=pathToTrack.split('/')[-1]
    openFile=mutagen.File(pathToTrack)
    if (openFile != None): 
        typeMime=openFile.mime        
        dictioMetadata=DefineMetadataFromMime(pathToTrack)
        if (dictioMetadata != None):
            track=ModelTrack(myFileName,dictioMetadata,typeMime)
            logging.info("ReadTrackFileAndTransform: transformation OK")
            return track
        else:
            logging.error("File: "+ pathToTrack+ " : No Metadata from file to extract")
    logging.error("File:"+ pathToTrack+ "impossible to read by mutagen")
    return None

def RecurExploreDirAndAddTrack(dbCollec, pathF):
    ''' Explore a directory recursively and add track to MongoDB bypass little file'''
    fList = os.listdir(pathF)
    for fi in fList:
        pathToFi=pathF+'/'+fi
        if os.path.isdir(pathToFi): # found a directory - recursive
            RecurExploreDirAndAddTrack(dbCollec, pathToFi)
        else:
            if os.stat(pathToFi).st_size > 512 * 1024: # found a file larger than 512kb
                myTrack=ReadTrackFileAndTransform(pathToFi)
                if (myTrack==None):
                    logging.warning("LoadLocalFilesToMongoDB: One file was missed")
                else:
                    try :
                        dbCollec.insert_one(myTrack.getDicAttTrack())
                        logging.info("insertion of the file: "+ pathToFi+" in mongoDB")
                    except :
                        print("Insertion DB Error",sys.exc_info())
                        logging.error("No insertion in mongoDB of :"+ pathToFi +"\n+"+ sys.exc_info())                    

def LoadLocalFilesToMongoDB():
    # CONFIGURATION localhost to set DevMongoDB initial data 
    try :
        mongoCl=MongoClient('localhost', 27017)
        db=mongoCl['MusicProj']
        collec=db.MetaDataMusic
        
        #mcb=gridfs.GridFS(db, 'TrackMusicBucket')
        
        # with fs.new_file(filename='file.txt',content_type='text/plain') as fp:
        # fp.write('New file
        # Explore your directory
        #myFileToAnalyze="06 What You Know About Richard D. James.mp3";
        #myTrack=ReadTrackFileAndTransform(myFileToAnalyze)
    except :
        print("Error configuration DB",sys.exc_info())
        logging.critical("Critic error can't connect to MongoDB, looks your conf DB" + sys.exc_info())
        return None
    RecurExploreDirAndAddTrack(collec,'.')
    return 1

if __name__ == '__main__':
    logging.basicConfig(filename='TransformationMusicTool.log', filemode='w', level=logging.ERROR)
    logging.info('Started To ReadAndTransform')
    os.chdir("../music/")
    
    LoadLocalFilesToMongoDB()
    #print(myTrack.dicAttTrack)
    logging.info('Finished to ReadAndTransform')
    pass