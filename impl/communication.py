# Responsavel pela comunicacao com o sistema CMPP
# a comunicacao se da atraves de uma interface serial

import abc
from enum import Enum, IntEnum, auto
from random import randint
from cmpp.impl.memmapping import CmppParam, CmppParamBundle
from cmpp.impl.datalink import CmppDataLinkerInterface
from typing import List
from time im


from enum import Enum, auto
class Enum_AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
class Protocol(Enum_AutoName):
    Posijet1 = auto()
    Posijet2 = auto()
    Auto_Detect = auto()


class CmppPacketInterface(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        '''
        :return: bytes of the packet (including checksum, duplicated esc, etc)
        '''
        pass

    @abc.abstractmethod
    @property
    def isCompleteAndValid(self) -> bool:
        '''
        :return: true if packet is complete and well formed, false otherwise
        '''




class CmppAvenue:
    def __init__(self, channel, port, protocol=Protocol.Posijet1):
        if channel > 63: channel=63
        self._channel = channel
        self._port = port
        self._protocol = protocol
        self._datalinker: CmppDataLinkerInterface   # initialized by self.transact

    @property
    def channel(self):
        return self._channel

    @property
    def port(self):
        return self._port

    @property
    def protocol(self):
        return self._protocol

    #if serial port has received data, send it to datalinker reception processor
    def update(self):
        pass

    def transact(self, paramBundle: CmppParamBundle):
        # choose appropriate data-link protocol
        from cmpp.impl.datalink import Posijet1
        if self.protocol == Protocol.Posijet1:
            self._datalinker = Posijet1(avenue=self)
        else:
            raise Transmission("Cmpp Data-link protocol choosed not supported")
        # Delegate transaction
        err_, bundle_ = self.datalinker.transact(paramBundle)
        return err_, bundle_

    def transmit(self, packet : CmppPacketInterface):
        #self.state. = receiptionCallBack
        pass






def transceiveCmpp(porta, direcao, canal, memmap, dadoL, dadoH):

    transaction_report = dict()
    transmission = dict()
    reception = dict()

    #todo: improve piping infra-structure

    pacote_envio_raw :bytes = criaPacote(
                        direcao, canal, memmap, dadoL, dadoH )
    #todo: document 'transaction data structure'
    pacote_enviado_parsed = parsePacote(pacote_envio_raw)
    #todo: if parsing has error don't send packet, handle error
    summary_info = interpretaPacoteEnviado(pacote_enviado_parsed)

    transmission[RawPacket] = pacote_envio_raw
    transmission[Parsed] = pacote_enviado_parsed
    transmission[Summary] = summary_info

    transaction_report[Transmission] = transmission

    #data-link
    pacote_recebido_raw :bytes = transmite_E_Recebe_Serial(porta, pacote_envio_raw)
    pacote_recebido_parsed = parsePacote(pacote_recebido_raw)
    resposta_interpretada = \
        interpretaPacoteRecebido(
            pacote_recebido_parsed,
            pacote_enviado_parsed)

    reception[RawPacket] = list(pacote_recebido_raw)
    reception[Parsed] = pacote_recebido_parsed
    reception[Summary] = resposta_interpretada

    transaction_report[Reception] = reception

    print('Transacao:')
    print(transaction_report, "\n")


    return transaction_report


def transmite_E_Recebe_Serial(porta, pacote_list):
    #envia
    for each in pacote_list:
        byte = bytes([each])
        sendByteThroughSerial(porta, byte)

    #aguarda retorno
    #sleep(0.5)

    #recebe
    bytes_recebidos : bytes = readBytesFromSerial(porta)
    return bytes_recebidos





def sendWordToCMPP(param: CmppParam, avenue: CmppAvenue):
    dadoL, dadoH = convertInt(param.value)
    direcao = DIRECAO_ENVIO
    result = transceiveCmpp(
        avenue.port, direcao, avenue.channel, param.key.memmap, dadoL, dadoH
    )
    return result

def sendBitToCMPP(param: CmppParam, avenue: CmppAvenue):
    value = param.value
    if (value >= 2): value=0 # todo: log error: type mismatch
    if value == 0:
        direcao = DIRECAO_MASCARA_RESETAR_BITS
    else:
        direcao = DIRECAO_MASCARA_SETAR_BITS
    value = value << int(param.key.memmap.startbit)
    dadoL, dadoH = convertInt(value)
    result = transceiveCmpp(
        avenue.port, direcao, avenue.channel, param.key.memmap, dadoL, dadoH
    )
    return result

def sendByteToCMPP(param: CmppParam, avenue: CmppAvenue):
    value = param.value
    param_ = param.key.name
    porta = avenue.port
    canal = avenue.channel

    if (value >= 256): value = 0  # todo: log error: type mismatch
    startbit = param.key.memmap.startbit
    comando = param.key.memmap.command
    bitlen = param.key.memmap.bitlen
    dadoL = int(0)
    dadoH = int(0)
    result = dict()

    #invariant
    if (startbit !=8 or startbit != 0): pass # todo:logo error: padding mismatch

    # Get current word from CMPP
    result = transceiveCmpp(
        porta, DIRECAO_SOLICITACAO, canal, param.key.memmap, dadoL, dadoH
    )
    if result[Transmission][Summary]['Tipo'] == 'Retorno com erro':
        pass #todo handle exception
    dadoL = result[Transmission][Parsed][State.DATA_LOW]
    dadoH = result[Transmission][Parsed][State.DATA_HIGH]

    # Overwrite byte I want to send
    if (startbit == 8): dadoH = value
    if (startbit == 0): dadoL = value

    # Send new information to CMPP
    result = transceiveCmpp(
        porta, DIRECAO_ENVIO, canal, param.key.memmap, dadoL, dadoH
    )
    return result


def sendParamToCmpp(param : CmppParam, avenue: CmppAvenue):
    value = param.value
    canal = avenue.channel
    porta = avenue.port
    if canal > 64: canal=64 #todo: log error 'channel overflow'
    if (type(value) is int):
        if value > 65535: value=0 #todo: log error 'value overflow'

    bitlen = param.key.memmap.bitlen
    if (bitlen == 16):
        result = sendWordToCMPP(param, avenue)
    elif (bitlen == 1):
        result = sendBitToCMPP(param, avenue)
    elif (bitlen == 8):
        print("Estrategia: Byte - Nao implementado")
        result = sendByteToCMPP(param, avenue)
    else:
        #todo: log error 'bitlen has no strategy, skiped!'
        DoNothing = 0
    return result







if __name__ == "__main__":

    from cmpp.impl.posReader import readPosTagTest

    paramBundle = readPosTagTest()
    avenue = CmppAvenue(channel=3, port='COM1')

    err, paramBundle = avenue.transact(paramBundle)
