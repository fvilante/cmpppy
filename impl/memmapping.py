# Le todos os drivers e encapsula em memmap requisitado

import toml
from drivers.CMPP00LG import Movimentador_Generico, CmppEnumInterface
from typing import Dict, List, Union, Optional




# todo: send this configuration to a toml. Include open-ended drivers
ConfigFile = {
    "CMPP00LG": '../drivers/CMPP00LG.toml',
}


def _readConfigFile(FileType) -> Dict[str, Union[int, str]]:
    with open(ConfigFile[FileType], 'r') as myfile:
        dict_ = toml.load(myfile)
    return dict_

def _getMemMap(param, driver='CMPP00LG'): #todo: remove this default
    dict_ = _readConfigFile(driver)
    #todo: validate memmap (if file has all fields)
    return dict_[param.name]




class CmppDriver:
    def __init__(self, name: str, funcionality : CmppEnumInterface):
        self._name = name
        self._funcionalidade = funcionality # ex. Movimentador_Generico

    def __repr__(self):
        return f'{self._name}'

    @property
    def allMemoryMap(self) -> Dict[str, Union[int, str]]:
        return _readConfigFile(self.name)

    @property
    def functionality(self):
        return self._funcionalidade

    def _makeKey(self, *, enumElement : CmppEnumInterface): # -> CmppKey:
        key_ = CmppKey(enumElement=enumElement, driver=self)
        return key_

    def _makePair(self, *, key, value: Optional[int] = None): #-> CmppPair:
        if (issubclass(type(key), CmppKey)):
            key_ = self._makeKey(enumElement=key._enumElement)
            pair_ = CmppPair(key=key_, value=value)
            return pair_
        else:
            raise TypeError()

    # helper facade class
    def makeParam(self, *, key : CmppEnumInterface=None, _keyStr: str=None, value: Optional[int] = None):
        if (key is None) and (_keyStr is None):
            raise ValueError("Necessary to give key **OR** _keyStr param")
        if _keyStr is None:
            cmppkey = self._makeKey(enumElement=key)
        else:
            key_cast = self.functionality(_keyStr)
            cmppkey = self._makeKey(enumElement=key_cast)
        return self._makePair(key=cmppkey, value=value)



    @property
    def name(self):
        return self._name


class MemMap:
    def __init__(self, rawDict: Dict[str, Union[int,str]]):
        self._dict = rawDict
        pass

    def __repr__(self):
        return f'{{' \
               f'desc={self.description}, ' \
               f'cmd={self.command}, ' \
               f'startBit={self.startbit}, ' \
               f'bitLen={self.bitlen}' \
               f'}}'

    @property
    def description(self):
        return self._dict['descricao']

    @property
    def command(self):
        return self._dict['comando']

    @property
    def bitlen(self):
        return self._dict['bitlen']

    @property
    def startbit(self):
        return self._dict['startbit']


class CmppKey:
    def __init__(self, enumElement, *, driver : CmppDriver):
        typecheck = issubclass(type(enumElement), CmppEnumInterface)
        if (typecheck):
            self._enumElement = enumElement
            self._driver = driver
        else:
            raise TypeError("enumElement precisa herdar da classe CmppEnumInterface")

    def __repr__(self):
        return f'{{{self.name}, driver={self._driver}}}'

    @property
    def name(self) -> str:
        return self._enumElement.name

    @property
    def memmap(self):
        return MemMap(self._driver.allMemoryMap[self.name])



class CmppPair:
    def __init__(self, *, key: CmppKey, value: int = None):
        self._key = key
        self._value = value

    def __repr__(self):
        return f'{{{self._key}: {self._value}}}'

    @property
    def key(self):
        return self._key

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, v: int):
        self._value = v

class CmppParam(CmppPair):
    pass


def dictToCmppParamList(dict_: Dict[str, Optional[int]], driver: CmppDriver) -> List[CmppParam]:
    list_ = []
    for keyStr, value in dict_.items():
        param = driver.makeParam(_keyStr=keyStr, value=value)
        list_.append(param)
    return list_

class CmppParamBundle:
    def __init__(self, dict_: Dict[str, Optional[int]], driver: CmppDriver):
        # Note: It is supposed that dict_.key's are already validated
        #       against CmppDriver
        self._dict = dict_
        self._driver = driver

    def __repr__(self):
        return  f'{{' \
                f'driver={self._driver}, ' \
                f'dict={self._dict}' \
                f'}}'

    @property
    def list(self):
        return dictToCmppParamList(self._dict, self._driver)

    def update(self, param: CmppParam):
        # Note: It is supossed that param is alread validated to have
        #       a valid 'key' attribute
        key = param.key.name
        value = param.value
        singleDict_ = { key : value }
        self._dict.update(singleDict_)


if __name__ == "__main__":

    driver = CmppDriver(name="CMPP00LG", funcionality=Movimentador_Generico)
    print(driver)

    # O parametro nomeado '_keyStr' esta reservado para uso
    # interno somente, prefira usar 'key' no lugar de '_keyStr'.
    # O motivo é que '_keyStr' gera erro em run-time, enquanto
    # 'key' gera erro em compile-time. Exemplo:
    param = driver.makeParam(
        #evite:
        _keyStr="Posicao_inicial", value=int(66)
    )
    param = driver.makeParam(
        #prefira:
        key=driver.functionality.Posicao_inicial, value=int(12)
    )


    print(param.key)
    print(param.value)
    print(param)
    print(param.key.memmap)
