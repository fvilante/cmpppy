# Load Drivers.json into memory
import json
from typing import List, Dict, NamedTuple, Any, Optional, Union
from toolz.dicttoolz import itemmap
from munch import Munch
def read_json():
    with open("Drivers.json", "r") as read_file:
        data = json.load(read_file)
    return data


#--------------
# DATA MODEL
#--------------

class Description(NamedTuple):
    uid: str
    Caption: str
    Doc: str

class MetaData(NamedTuple):
    Interfaces: List[str]
    Tags: List[str]

class MemRegion(NamedTuple):
    StartWord: int
    StartBit: int
    BitLength: int


class Limits(NamedTuple):
    Maximum: int
    Minimum: int

class TypeCast_Uint16(NamedTuple):
    Type: str
    Limits: Limits

class Option(NamedTuple):
    Label: str
    Value: int

class TypeCast_OneOf(NamedTuple):
    Type: str
    Options: List[Option]

class Units(NamedTuple):
    UOM: str

class Parameter(NamedTuple):
    Description: Description
    MetaData: MetaData
    MemRegion: MemRegion
    TypeCast: Union[TypeCast_OneOf, TypeCast_Uint16]
    Units: Units

Parameters = List[Parameter]

# ===================
# functions
# ===================

def description(dic) -> Description:
    return Description(**dic)
def metaData(dic) -> MetaData:
    return MetaData(**dic)
def memRegion(dic) -> MemRegion:
    return MemRegion(**dic)
def limits(dic) -> Limits:
    return Limits(**dic)
def options(dic) -> List[Option]:
    list_ = []
    for option in dic: #dic is a list of option
        label = option['Label']
        value = option['Value']
        list_.append(Option(Label=label,Value=value))
    return list_
def typeCast(dic) -> Union[TypeCast_OneOf, TypeCast_Uint16]:
    if dic['Type'] == 'UInt16':
        limits_ = limits(dic['Limits'])
        return TypeCast_Uint16(Type='UInt16', Limits=limits_)
    elif dic['Type'] == "OneOf":
        options_ = options(dic['Options'])
        return TypeCast_OneOf(Type='OneOf', Options=options_)
def units(dic) -> Units:
    return Units(**dic)

def parameter(param) -> Parameter:
    description_ = description(param['Description'])
    metaData_ = metaData(param['MetaData'])
    memRegion_ = memRegion(param['MemRegion'])
    typeCast_ = typeCast(param['TypeCast'])
    units_ = units(param['Units'])
    res = ( description_, metaData_, memRegion_, typeCast_, units_)
    return Parameter(*res)

def parameters(params) -> Parameters:
    return list(map(parameter,params))



# -------------------------
#  Test
# -------------------------

if __name__ == "__main__":
    data = read_json()
    dat = data['Drivers'][0]['Parameters'][0]
    print(dat)
    im = parameter(dat)
    print(im)
    print(im.MemRegion.StartWord)
    print(im.Description.Caption)
    print(im.MetaData.Tags)

    # parameters list

    print("---------------")
    params = data['Drivers'][0]['Parameters']
    p = parameters(params)
    print(p)

    pass
