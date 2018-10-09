# Model Data of MemMap format:
# Cast MemMap dict to add some (type) safety.
from typing import NamedTuple, List, Tuple, Union
#from CMPP.MemMaperLoader import loadCMPPDriver
from functools import singledispatch


ErrorMsg = str
IsValid = bool
Validation = Tuple[IsValid, ErrorMsg]

#Helpers
def valid() -> Validation:
    return (True, "Data is Valid")
def error(msg: ErrorMsg) -> Validation:
    return (False, "Erro no DriverCMPP: " + msg)


@singledispatch
def isValid(type_) -> Validation:
    return error(f'Verificação de chave com validador inexistente. [{type_}]')



# ======================
# Data Model
# ========================


FileFormatType = str # expected 'CMPPMemMapFile'
Version = Tuple[int,int,int]
DriverTarget = str # example: 'CMPP00LG'
class Header(NamedTuple):
    fileFormatType: FileFormatType
    fileFormatVersion: Version
    driverRevision: Version
    driverTarget: DriverTarget

    def isValid(self):
        return isValid(self)
    pass


erro_header = "[Header] -> "
erro_header_1 = erro_header + "Versao deve ser no formato [int,int,int], exemplo: [0,1,5]"
erro_header_2 = erro_header + "Versao deve ser uma lista no formato [int,int,int] exemplo: [0,1,5]"
erro_header_3 = erro_header + "O campo FileFormatType deve conter a string 'CMPPMemMapFile' (atente para igualar maisculas e minusculas)"
erro_header_4 = erro_header + 'O campo Driver.Target deve conter uma string. Ex: Driver.Target = "CMPP00LG"'
@isValid.register(Header)
def _(header: Header) -> Validation:
    # check target is string
    if not isinstance(header.driverTarget, str):
        return error(erro_header_4)
    # check versions
    for version in [header.driverRevision, header.fileFormatVersion]:
        if isinstance(version, list):
            if not len(version) == 3:
                return error(erro_header_1)
            pass
        else:
            return error(erro_header_2)
    # check FileFormatTypee
    if not header.fileFormatType == 'CMPPMemMapFile':
        return error(erro_header_3)
    #else
    return valid()




UUID = str  # todo: accept only str 'A_Z, a_z, 0_9', reject otherwise
Caption = str
Doc = str
class Description(NamedTuple):
    uuid: UUID
    caption: Caption
    doc: Doc

    def isValid(self):
        return isValid(self)
    pass


erro_desc = "[Parameter.Description] -> "
erro_desc_1 = erro_desc + 'As chaves uuid, caption e doc devem ser strings. Exemplo: Caption = "Posicao inicial"'
erro_desc_2 = erro_desc + "UUID possui um caractere invalid. Os caracteres válidos são [A-Z][a-z][0-9][_]. Exemplo: 'Posicao_inicial'"
@isValid.register(Description)
def _(desc: Description) -> Validation:
    # checa se é string
    str_ = [desc.uuid, desc.caption, desc.doc]
    for each in str_:
        if not isinstance(each, str):
            return error(erro_desc_1)
    # checa se UUID contem apenas caracteres considerados validos
    import re  # For more on regex see: https://regex101.com/
    regex = r"([a-z]|[A-Z]|[0-9]|_)*"
    if not bool(re.fullmatch(regex, desc.uuid, flags=0)):
        return error(erro_desc_2)
    return valid()






Interface = List[str]
Tag = List[str]
class MetaData(NamedTuple):
    interface: Interface
    tag: Tag

    def isValid(self):
        return isValid(self)


erro_inter = "[Parameter.Interface] -> "
erro_inter_1 = erro_inter + 'A chave Interface deve ser uma lista de strings. Ex: Interface = ["Movimentador Generico","Dosador Silicone"]'
@isValid.register(MetaData)
def _(inter: MetaData) -> Validation:
    # checa se é lista
    for list_ in [inter.interface, inter.tag]:
        if not isinstance(list_, list):
            return error(erro_inter_1)
        else:
            # checa se cada elemento da lista é string
            for elem in list_:
                if not isinstance(elem, str):
                    return error(erro_inter_1)
    # ok
    return valid()




StartWord = int
StartBit = int  # todo: validate to 0~15
BitLength = int
class MemRegion(NamedTuple):
    startWord: StartWord
    startBit: StartBit
    bitLength: BitLength

    def isValid(self):
        return isValid(self)

erro_memreg = "[Parameter.MemRegion] -> "
erro_memreg_1 = erro_memreg + 'As chaves StartWord, StartBit e BitLengh devem ser inteiros positivos.'
erro_memreg_2 = erro_memreg + 'A chave StartBit deve estar entre 0 e 15'
@isValid.register(MemRegion)
def _(m: MemRegion) -> Validation:
    # checa se sao inteiros positivos
    for each in [m.startWord, m.startBit, m.bitLength]:
        if not isinstance(each, int):
            return error(erro_memreg_1)
        elif not each >= 0:
            return error(erro_memreg_1)
    # checa se startbit está entre 0 e 15
    if not (m.startBit >= 0 and m.startBit <= 15):
        return error(erro_memreg_2)
    return valid()



Value = int # todo: value could not be greather than Memory-Region



class Default(NamedTuple):
    value: Value

    def isValid(self):
        return isValid(self)

erro_default = "[Parameter.Default] -> "
erro_default_1 = erro_default + 'A chave Value deve ser um inteiro positivo.'
@isValid.register(Default)
def _(d: Default) -> Validation:
    # checa se sao inteiros positivos
    for each in [d.value]:
        if not isinstance(each, int):
            return error(erro_default_1)
        elif not each >= 0:
            return error(erro_default_1)
    return valid()




Type = str # todo: Validate to 'Uint16' or 'OneOf'



class Uint16(NamedTuple):
    valueMin: Value
    valueMax: Value
    type: Type = 'Uint16'

    def isValid(self):
        return isValid(self)

erro_uint16 = "[Parameter.Uint16] -> "
erro_uint16_1 = erro_uint16 + "A chave Type precisa conter exatamente a string 'Uint16'"
erro_uint16_2 = erro_uint16 + "As chaves 'Value.Min' e 'Value.Max' precisam ser inteiros positivos"
erro_uint16_3 = erro_uint16 + "As chave 'Value.Min' precisa ser menor ou igual a chave 'Value.Max'"
@isValid.register(Uint16)
def _(d: Uint16) -> Validation:
    # checa se type
    if not d.type == 'Uint16':
        return error(erro_uint16_1)
    # checa se sao inteiros positivos
    for each in [d.valueMax, d.valueMin]:
        if not isinstance(each, int):
            return error(erro_uint16_2)
        elif not each >= 0:
            return error(erro_uint16_2)
    # checa se min <= max
    if not (d.valueMin <= d.valueMax):
        return error(erro_uint16_3)
    # ok
    return valid()



OptionCaption = str
class Option(NamedTuple):
    value: Value
    caption: OptionCaption

    def isValid(self):
        return isValid(self)

erro_option = "[Parameter.Option] -> "
erro_option_1 = erro_option + "As chave 'Valor' deve ser um inteiro positivo"
erro_option_2 = erro_option + "As chave 'Caption' deve ser do tipo 'String'"
@isValid.register(Option)
def _(d: Option) -> Validation:
    # checa se .Value é inteiro positivo
    if not isinstance(d.value, int):
        return error(erro_option_1)
    elif not d.value >= 0:
        return error(erro_option_1)
    # checa se .Caption é string
    if not isinstance(d.caption, str):
        return error(erro_option_2)
    # ok
    return valid()


class OneOf(NamedTuple):
    options: List[Option] # todo: validation caption and value can't repeat in the same options list
    type: Type = 'OneOf'

    def isValid(self):
        return isValid(self)

erro_oneOf = "[Parameter.OneOf] -> "
erro_oneOf_1 = erro_oneOf + "A chave Type precisa conter exatamente a string 'OneOf'"
erro_oneOf_2 = erro_oneOf + "A chave 'Options' não pode possuir elementos repetidos no campo 'Value'"
erro_oneOf_3 = erro_oneOf + "A chave 'Options' não pode possuir elementos repetidos no campo 'Caption'"
@isValid.register(OneOf)
def _(d: OneOf) -> Validation:
    # checa se type
    if not d.type == 'OneOf':
        return error(erro_oneOf_1)
    # check if option's values are unique
    others: List[Value] = []
    for option in d.options:
        a = option.value
        if a in others:
            return error(erro_oneOf_2)
        else:
            others.append(a)
    others: List[Value] = []
    # check if option's captions are unique
    for option in d.options:
        a = option.caption
        if a in others:
            return error(erro_oneOf_3)
        else:
            others.append(a)
    # ok
    return valid()

class TypeCast(NamedTuple):
    typeCast: Union[Uint16, OneOf]

    def isValid(self):
        return isValid(self)

@isValid.register(TypeCast)
def _(t: TypeCast) -> Validation:
    return t.typeCast.isValid()





class Parameter(NamedTuple):
    description: Description
    metaData: MetaData
    memRegion: MemRegion
    default: Default
    typeCast: TypeCast

    def isValid(self):
        return isValid(self)

@isValid.register(Parameter)
def _(p: Parameter) -> Validation:

    return ( p.description.isValid()
             and p.metaData.isValid()
             and p.memRegion.isValid()
             and p.default.isValid()
             and p.typeCast.isValid()
             )



class Driver(NamedTuple):
    header: Header
    parameters: List[Parameter]

    def isValid(self):
        return isValid(self)

@isValid.register(Driver)
def _(d: Driver) -> Validation:
    # header is valid?
    c1 = d.header.isValid()
    # each of parameters are valid?
    parameters = [each for each in d.parameters]
    k:List[bool] = []
    for param in parameters:
        k.append(param.isValid())
    c2 = all(k)
    # result
    return (c1 and c2)

if __name__=="__main__":

    #data = loadCMPPDriver('./MemMap/CMPP00LG.toml')

    from CMPP.MemMap.Caster import CMPPDriver
    file = './Drivers/CMPP00LG.toml'
    driver = CMPPDriver(file)

    header = driver.getHeader()
    print(header.isValid())
    print(type(header.driverTarget))
    parameter = driver._getParameterByIndex(1)
    print(parameter.description.isValid())
    print(parameter.metaData.isValid())
    print(parameter.memRegion.isValid())
    print(parameter.default.isValid())
    print(parameter.typeCast)
    print("--------")
    print(parameter.typeCast.isValid())
    print(parameter.isValid())
    print(driver)


    pass





