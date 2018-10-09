from CMPP.MemMap import CMPPDriver
from CMPP.pos import PosFile
from SerialPort import PortHandler, PortsManager, SerialPortId, PortConfiguration, BaudRate
from Common.Byte import Byte, Bytes
from CMPP.Protocol import encode, FrameOutgoing, Direcao, Canal, Comando, DadoH, DadoL
from typing import NamedTuple, Any, Dict
from enum import Enum


class TranscationType(Enum):
    Set = 1
    Get = 2

Parameters = Dict[str, Any]

class Bundle(NamedTuple):
    transactionType: TranscationType
    parameters: Parameters
    memmap: CMPPDriver
    channel: Canal

def sendToPort(bundle: Bundle, port1: PortHandler) -> bool:
    params = bundle.parameters
    memmaps = bundle.memmap
    channel = bundle.channel

    for param, value in params.items():
        print(param, value)
        memmap = memmaps.getParameterByUUID(param)
        #print(memmap['MemRegion'])
        startWord = memmap['MemRegion']['StartWord']
        startBit = memmap['MemRegion']['StartBit']
        bitLength = memmap['MemRegion']['BitLength']
        print(startWord, startBit, bitLength)




if __name__=="__main__":

    # Create Port Spec
    portId1 = SerialPortId('COM5', PortConfiguration(BaudRate.Bps_9600))
    portId2 = SerialPortId('COM4', PortConfiguration(BaudRate.Bps_9600))
    manager = PortsManager()
    port1, error1 = manager.requestPortHandler(portId1)
    port2, error2 = manager.requestPortHandler(portId2)
    print(error1)
    print(error2)
    data = [Byte(65), Byte(67), Byte(68)]
    port1.write(data)
    print(port2.read(4))


    # Load MemMap
    memMap = CMPPDriver("./MemMap/Drivers/CMPP00LG.toml")

    # Load POSFile
    posfile = PosFile("./pos/Files/standard.toml")

    # Load program 0 from PosFile
    program = posfile.getProgramByIndex(0)

    # Change program in-memory
    program['Body'].update({'Logica_de_sinal_de_impressao': 12})
    params = program['Body']
    print(params)

    # send to channel 2
    canal = Canal(2)
    bundle = Bundle(TranscationType.Set, params, memMap, canal)
    sendToPort(bundle, port1)

    
    # Transfer parameters do CMPP given channel
    
    #print(memMap)
    #print(posfile)
    #print(program['Body'])

