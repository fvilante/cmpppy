from drivers.Parameters import parameters, Parameters
from typing import NamedTuple, List, Dict, Any

# ================
# Data Model
# ================

class Version(NamedTuple):
    string: str
    @property
    def mayor(self):
        return self.value.split('.')[0]
    @property
    def minor(self):
        return self.value.split('.')[1]
    @property
    def revision(self):
        return self.value.split('.')[2]
    @property
    def versionFormated(self):
        return self.value.split('.')

class Info(NamedTuple):
    uid: str
    Version: Version
    Caption: str
    Target: str

class Driver(NamedTuple):
    Info: Info
    Parameters: Parameters

    def __repr__(self):
        return str(self.Info.Caption)

class Header(NamedTuple):
    Format: str
    Schema_version: Version

Drivers = List[Driver]

class DriversDataObject(NamedTuple):
    Header: Header
    Drivers: Drivers




# ================
#  Functions
# ================

def formatVersion(dic,vkey:str): #-> Dict[Any]
    d = dic
    v = d[vkey]
    d[vkey] = Version(v)
    return d

def info(dic) -> Info:
    d = formatVersion(dic,'Version')
    return Info(**d)

def driver(dic) -> Driver:
    info_ = info(dic['Info'])
    parameters_ = parameters(dic['Parameters'])
    return Driver(Info=info_, Parameters=parameters_)

def drivers(dic) -> Drivers:
    return list(map(driver,dic))

def header(dic) -> Header:
    d = formatVersion(dic, 'Schema_version')
    return Header(**d)


#main Function - Loads all the json driver data information
def loadAll(dic) -> DriversDataObject:
    header_ = header(dic['Header'])
    drivers_ = drivers(dic['Drivers'])
    return DriversDataObject(Header=header_, Drivers=drivers_)

# ================
#  Test
# ================

if __name__ == "__main__":
    from drivers.Parameters import read_json

    # driver
    data = read_json()
    dat = data['Drivers']
    d = driver(dat[0])
    print(d)
    print("***********")

    # drivers
    ds = drivers(dat)
    print(ds)

    # loadAll
    all = loadAll(data)
    print(all)
    print("##########")
    print(all.Header.Schema_version.string)
