# Protocolo 1 Transmitter part
from typing import NamedTuple
from enum import Enum
from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from CMPP.Protocol.DataLiinkEncode import encode
from CMPP.Protocol.DataLinkDecode import FrameReceived, Decoder

# ----------------------------------
# Outgoing
# ----------------------------------


class Direcao(Enum):
    Solicitacao = (0 << 6) + (0 << 7)
    Mascara_Resetar_Bits = (0 << 6) + (1 << 7)
    Mascara_Setar_Bits = (1 << 6) + (0 << 7)
    Direcao_Envio = (1 << 6) + (1 << 7)

class Canal:
    def __init__(self, canal: int) -> None:
        if canal>63:
            raise ValueError("Número do canal precisa estar entre 0 e 63 inclusive.")
        else:
            self._value: int = canal

Comando = Byte
DadoH = Byte
DadoL = Byte

class FrameOutgoing(NamedTuple):
    direcao: Direcao
    canal: Canal
    comando: Comando #Byte
    dadoL: DadoH #Byte
    dadoH: DadoL #Byte


    def __bytes__(self):
        direcaoECanal = bytes([self.direcao.value + self.canal._value])
        return direcaoECanal + bytes(self.comando) + bytes(self.dadoL) + bytes(self.dadoH)



if __name__=="__main__":

    frame = FrameOutgoing(Direcao.Direcao_Envio, Canal(1), Comando(20), DadoL(65), DadoH(67))
    print(encode(frame))






    pass