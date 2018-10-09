# Type casts the loaded TomL/MemMap data file to a more type-safety object inside Python
from CMPP.MemMap.DataModel import Header, UUID, Parameter, Description, MetaData, MemRegion, Default, TypeCast, Uint16, OneOf, Option, Driver
from CMPP.MemMap.Loader import loadCMPPDriver
from tomlkit.toml_document import TOMLDocument
from typing import Union, List, Optional

FilePath = str   #exemple: './MemMap/CMPP00LG.toml'

class CMPPDriver:

    def __init__(self, filename: FilePath) -> None:
        # Dict-Like format / See: TomlKit Documentation on github for more
        self._dataBase: TOMLDocument = loadCMPPDriver(filename)

    def getHeader(self) -> Header:
        type_ = self._dataBase['Header']['File']['Format']['Type']
        format_ = self._dataBase['Header']['File']['Format']['Version']
        revision_ = self._dataBase['Header']['Driver']['Revision']
        target_ = self._dataBase['Header']['Driver']['Target']
        return Header(type_, format_, revision_, target_)

    def getParameterByUUID(self, uuid: UUID) -> dict:
        for parameter in self._dataBase['Parameter']:
            if parameter['Description']['UUID'] == uuid:
                return parameter

    def _getParameterByIndex(self, idx: int) -> Optional[Parameter]:
        try:
            parameter = self._dataBase['Parameter'][idx]
        except IndexError:
            return None
        return self.getParameter(parameter['Description']['UUID'])

    def getParameter(self, uuid: UUID) -> Parameter:
        data = self.getParameterByUUID(uuid)
        d = data['Description']
        description = Description(d['UUID'], d['Caption'], d['Doc'])
        m = data['MetaData']
        metaData = MetaData(m['Interface'], m['Tag'])
        r = data['MemRegion']
        memRegion = MemRegion(r['StartWord'], r['StartBit'], r['BitLength'])
        f = data['Default']
        default = Default(f['Value'])


        # todo: This polimorphic behaviour is a potential source of dynamic type error. What can be done to improve safety?
        typeCast = data['TypeCast']
        type_: str = data['TypeCast']['Type']
        obj: Union[OneOf, Uint16] = None
        if type_ == 'Uint16':
            obj = Uint16(typeCast['Value']['Min'], typeCast['Value']['Max'])
        elif type_ == 'OneOf':
            options: List[Option] = []
            for option in typeCast['Options']:
                options.append(Option(option['Value'], option['Caption']))
            obj = OneOf(options)
        else:
            raise TypeError(f"Erro de interpretacao do arquivo MemMap: TypeCast '{type_}' não é reconhecido no parametro -> UUID:[{description.uuid}]")

        typeCast_ = TypeCast(obj)

        return Parameter(description, metaData, memRegion, default, typeCast_)


if __name__=="__main__":

    file = './Drivers/CMPP00LG.toml'
    data = loadCMPPDriver(file)
    print(data['Parameter'][0]['Description']['UUID'])

    driver = CMPPDriver(file)
    print('*******')
    header = driver.getHeader()
    print(header)
    uuid = 'Posicao_final'
    print(driver.getParameterByUUID(uuid))
    print("-----------")
    param = driver.getParameter(uuid)
    print(param)
    print(param.memRegion)
    print(param.typeCast)
    print("-----------")
    print(driver._getParameterByIndex(0))
    print(driver._getParameterByIndex(100))
    print("-----------")
    print(driver._getParameterByIndex(1).typeCast)
    pass