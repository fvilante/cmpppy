from typing import NamedTuple, List, Any, Optional, Dict,Tuple
from CMPP.MemMap.Loader import loadCMPPDriver as loadTOMLFile

class FileHeader(NamedTuple):
    fileFormat: str
    formatVersion: Tuple[int,int,int]

class ProgramHeader(NamedTuple):
    pass

class Program(NamedTuple):
    header: ProgramHeader
    params: Dict[str, Any]

class Programs(NamedTuple):
    program_list: List[Program]

UUID = str
class ProgramHeader(NamedTuple):
    uuid: UUID
    memMapUUID: UUID

ProgramBody = Dict[str, Any]

class Program(NamedTuple):
    header: ProgramHeader
    body: ProgramBody

class PosFile:
    def __init__(self, filePath: str) -> None:
        self._data : Dict[str, Any] = loadTOMLFile(filePath)

    def getProgramByIndex(self, index: int) -> Optional[Program]:
        try:
            return self._data['POS'][index]
        except:
            return None

    def getProgramByUUID(self, uuid: str) -> Optional[Program]:
        for program in self._data['POS']:
            if program['Header']['UUID'] == uuid:
                return program
        return None



if __name__=='__main__':


    posFile = PosFile('./Files/standard.toml')
    print(posFile.getProgramByIndex(0))

    #print(data['POS'][0]['Header'])
    print(posFile.getProgramByUUID('Base'))

    pass



