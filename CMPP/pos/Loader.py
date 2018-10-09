from tomlkit import dumps
from tomlkit import parse, loads
from tomlkit.toml_document import TOMLDocument


def readFile(filename: str) -> str:
    # file name ex: './Files/standard.toml'
    with open(filename, 'r') as myfile:
        data = myfile.read()
    return data

def parseData(data: str) -> TOMLDocument:
    return parse(data)

def loadCMPPDriver(filename: str) -> TOMLDocument:
    s = readFile(filename)
    return parseData(s)

if __name__=='__main__':

    doc = loadCMPPDriver('./Files/standard.toml')

    params = doc['POS'][0]['Body']

    print(list(params.keys()))
    print(params)

    pass
