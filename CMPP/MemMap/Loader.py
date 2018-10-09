from tomlkit import dumps
from tomlkit import parse, loads
from tomlkit.toml_document import TOMLDocument


def readFile(filename: str) -> str:
    # file name ex: './MemMap/CMPP00LG.toml'
    with open(filename, 'r') as myfile:
        data = myfile.read()
    return data

def parseData(data: str) -> TOMLDocument:
    return parse(data)

def loadCMPPDriver(filename: str) -> TOMLDocument:
    s = readFile(filename)
    return parseData(s)

if __name__=='__main__':

    doc = loadCMPPDriver('./Drivers/CMPP00LG.toml')

    print(doc["Header"]["Driver"]["Target"])

    print(doc)

    print("********")
    print(doc['Parameter'][1])
    print("********")
    print(doc['Header']['File']['Format']['Type'])

    pass
