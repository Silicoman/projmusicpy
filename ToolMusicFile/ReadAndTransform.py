import os
import sys
import logging

import mysql.connector
from mutagen.easyid3 import EasyID3
import mutagen


from pymongo import MongoClient

#import magic
from ToolMusicFile.ModelTrack import ModelTrack

#global fields=["title","artist","album","album artist","tracknumber", "date","genre", "bpm"]
''' RESUME OF THE EXECUTION FILE: READ FILES & TRANSFORM THEM & INSERT THEM
-- DEFINE configuration Database + Files path
       > LoadLocalFilesToDB()
    -- Open connexion to DB
    -- define your fonction InsertDB 
        >DefineInsertDB()
        -- if MongoDB
            >addTrackToDBMongoDB
        -- if Mysql
            >addTrackToDBMysql
            
-- Explore your path to find files to add
    > RecurExploreDirAndAddTrack()

    -- Read your track file and insert it to DB
        > ReadTrackFileAndTransform()
            -- Read Metadata/Fields File
                > DefineMetadataFromMime()

'''

def AddTrackToDBMysql(track,cnx):
    fields=["title","artist","album","album artist","length","tracknumber", "date","genre", "bpm","pathdir"]
    cursor = cnx.cursor()
    
    # BUILD AN INSERT SQL
    addTrackBegin = "INSERT INTO MetadataMusic ("
    addTrackEnd = "VALUES ("
    dataTrack = {}
    
    for field in track.dicAttTrack.keys():
        if (field in fields):
            addTrackBegin += ( field +", ")
            addTrackEnd += ("%(" + field + ")s, " )
            dataTrack[field] = track.dicAttTrack[field]


    addTrack=addTrackBegin[:-2] + ") " + addTrackEnd[:-2] + ")"
    cursor.execute(addTrack, dataTrack)
    cnx.commit()
    cursor.close()
    return 1;


def AddTrackToDBMongoDB(track,cnx):
    try :
        cnx.insert_one(track.getDicAttTrack())
        logging.info("insertion of the file: "+ track._getpath()+" in mongoDB")
    except :
        print("Insertion DB Error",sys.exc_info())
        logging.error("No insertion in mongoDB of :"+ track._getpath() +"\n+"+ sys.exc_info())
        

def DefineInsertDB(selectionDB):
        if (selectionDB=='mysql'):
            return AddTrackToDBMysql
        elif (selectionDB=='mongodb'):
            return AddTrackToDBMongoDB
        else:
            logging.warning("No function insert specific to your DB")
            return None

        
def DefineMetadataFromMime(myFile):
    ''' define metadata/tags of audio file and put value in a dict,
        operation depending of Mime Type'''
    dictionaryMetadata={}
    typeMime=mutagen.File(myFile).mime
    dictionaryMetadata['length']=int(mutagen.File(myFile).info.length)
    dictionaryMetadata['pathdir']=os.path.abspath(myFile)
    # CASE MP3
    if ('audio/mp3' in typeMime):
        try :
            tags=EasyID3(myFile)
            for i in tags. keys():
                dictionaryMetadata[i]=tags.get(i)[0] # 0 because tagValue is a list, takes directly the first value
            logging.info('From DefineMetadataFromMime: good extraction tags from the file: '+myFile)
            return dictionaryMetadata;
        except :
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

 
def RecurExploreDirAndAddTrack(functionInsertDB,cnx, pathF):
    ''' Explore a directory recursively and add track to MongoDB bypass little file'''
    fList = os.listdir(pathF)
    for fi in fList:
        pathToFi=pathF+'/'+fi
        if os.path.isdir(pathToFi): # found a directory - recursive
            RecurExploreDirAndAddTrack(functionInsertDB,cnx, pathToFi)
        else:
            if os.stat(pathToFi).st_size > 512 * 1024: # found a file larger than 512kb
                myTrack=ReadTrackFileAndTransform(pathToFi)
                if (myTrack==None):
                    logging.warning("LoadLocalFilesToMongoDB: One file was missed")
                else:
                    functionInsertDB(myTrack,cnx)                 


def LoadLocalFilesToDB(selectionDB):
    # CONFIGURATION localhost to set DevMongoDB/Mysql initial data
        cnx=object
        print(selectionDB)
        if (selectionDB=='mongoDB'):
            try:
                mongoCl=MongoClient('localhost', 27017)
                db=mongoCl['MusicProj']
                cnx=db.MetaDataMusic
            except Exception:
                print("Error configuration DB",sys.exc_info())
                logging.critical("Critic error can't connect to Database, looks your conf DB" +
                                  sys.exc_info())

        elif (selectionDB=="mysql"):

            try :
                cnx = mysql.connector.connect(user='adminMusicProj', password='adm1nsql!',
                              host='127.0.0.1',port='3306',
                              database='musicproj')
            except mysql.connector.Error :
                print("Error configuration DB",sys.exc_info())
                logging.critical("Critic error can't connect to Database, looks your conf DB" +
                                 sys.exc_info())
 
        else:
            logging.warning("Warning no databse connexion, looks your conf DB")
            return None
        functionInsert=DefineInsertDB(selectionDB)
        RecurExploreDirAndAddTrack(functionInsert,cnx,'.')
        cnx.close()
        

                                    
if __name__ == '__main__':
    fields = ["title","artist","album","albumartist","tracknumber", "date","genre", "bpm"]
    logging.basicConfig(filename='TransformationMusicTool.log', filemode='w', level=logging.INFO)
    logging.info('Started To ReadAndTransform')
    os.chdir("../music/")
    
    LoadLocalFilesToDB('mongodb')
    logging.info('Finished to ReadAndTransform')
    pass