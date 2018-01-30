
class ModelTrack(object):
    '''
    Model to object Track with a dictionnary of metadata values:
    -album;    -bpm;    -title
    -artist    -tracknumber;
    -genre;    -date;
    '''
    objectID=0
    
    def __init__(self, nameFile,dicAtt,mimeArg):
        ''' Constructor 
        +1 ID for each new track
        '''
        self.objectID+=1
        self.setNameFile(nameFile)
        self.setDicAttTrack(dicAtt)
        self.setMimeTypeList(mimeArg)


    # SETTER & GETTER & DOCSTRING
    def getMimeTypeList(self):
        return self.__mimeTypeList


    def setMimeTypeList(self, value):
        self.__mimeTypeList = value

    def getNameFile(self):
        return self.__nameFile

    def setNameFile(self, value):
        self.__nameFile = value

    # properties DicAtt == metadata track
    def getDicAttTrack(self):
        return self.__dicAttTrack

    def setDicAttTrack(self, value):
        self.__dicAttTrack = value

    def delDicAttTrack(self):
        del self.__dicAttTrack

    
    dicAttTrack = property(getDicAttTrack, setDicAttTrack, delDicAttTrack, 
                           "dicAttTrack's docstring: dictionnary attribut metadata track")
    nameFile = property(getNameFile, setNameFile, None,
                        "nameFile's docstring: origin name file")
    mimeTypeList = property(getMimeTypeList, setMimeTypeList, None, 
                        "mimeTypeList's docstring: list mime File")
    
