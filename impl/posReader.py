#creates POS object into memory

import toml
from impl.memmapping import CmppDriver, CmppParam, CmppParamBundle, dictToCmppParamList
from typing import List, Dict, Optional, Any



def _readPosFile(file: str) -> Optional[Dict[str, Any]]:
    with open(file, 'r') as myfile:
        d = toml.load(myfile)
    return d



def ReadPostagToDict(nome: str, file: str) -> Dict[str, Optional[int]]:
    dict_ = _readPosFile(file)
    original_ = dict_['POS'][nome]
    Inhirit_ = original_.pop('Inhirit', None)
    if Inhirit_ != None:
        # Note: Reintraint function!
        base_ = ReadPostagToDict(Inhirit_, file)
        override_ = base_
        override_.update(original_)
        result_ = override_
    else:
        result_ = original_
    return result_



def readPosTag(tagName: str, file: str, driver: CmppDriver):
    dict_ = ReadPostagToDict(tagName, file)
    list_ = dictToCmppParamList(dict_, driver)
    return list_



class PosFile:
    def __init__(self, file : str, driver: CmppDriver):
        self._file = file
        self._driver = driver

    def __repr__(self):
        return f'{{file={self._file}: driver={self._driver}}}'

    def readTag(self, tagName: str) -> CmppParamBundle:
        dict_ = ReadPostagToDict(tagName, self._file)
        paramBundle_ = CmppParamBundle(dict_, self._driver)
        return paramBundle_

    @property
    def tagsList(self):
        dict_ = _readPosFile(self._file)['POS']
        list_ = []
        for tag, value in dict_.items(): list_.append(tag)
        return list_


def readPosTagTest() -> List[CmppParam]:
    from impl.posReader import PosFile
    from impl.memmapping import Movimentador_Generico
    driver = CmppDriver("CMPP00LG", funcionality=Movimentador_Generico)
    pos = PosFile('../pos/standard.toml', driver)
    return pos.readTag('referenciar_z')



if __name__ == "__main__":

    #read pos file-tag
    from impl.memmapping import CmppDriver, Movimentador_Generico
    driver = CmppDriver("CMPP00LG", funcionality=Movimentador_Generico)
    pos = PosFile('../pos/standard.toml', driver)
    paramBundle = pos.readTag('referenciar_z')

    #change one parameter value
    param = driver.makeParam(key = driver.functionality.Modo_continuo_passo_a_passo)
    param.value = 1
    paramBundle.update(param)

    #inspect object
    print(paramBundle)

    #to interate over paramBundle you need to extract a list
    list_ = paramBundle.list

    #you alse get a list of avaliable tags that can me extract from Pos object (toml file)
    print("")
    print(pos.tagsList)


    pass