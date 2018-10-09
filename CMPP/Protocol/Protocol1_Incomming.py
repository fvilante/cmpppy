# Protocolo 1 Receiption part
from typing import NamedTuple
from enum import Enum
from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from CMPP.Protocol.DataLiinkEncode import encode
from CMPP.Protocol.DataLinkDecode import FrameReceived, Decoder



class Status(Enum):
    Referenciado = 0
    Posicao_Alcancada = 1
    Referenciando = 2
    Direcao_Do_Movimento_Eh_Positiva = 3
    Movimento_Acelerado = 4
    Movimento_Desacelerado = 5
    Reservado = 6
    Evento_De_Erro_Consulte_Mascara_De_Erro = 7
    # de 8 a 15 sao reservados

class ControleSerial(Enum):
    Start = 0
    Stop = 1
    Pausa = 2
    Modo_manual = 3
    Teste_de_impressão = 4
    Reservado_para_aplicações_especiais = 5
    Salva_os_parâmetro_na_EEprom = 6
    # 7 a 15 reservado


class MascaraDeErro(Enum):
    Sinal_de_Start_externo = 0
    Sinal_de_start_diversos = 1
    Sensor_de_giro_por_falta = 2
    Sensor_de_giro_por_excesso = 3
    Sinal_de_Impressão = 4
    Erro_de_comunicação_ocorrido_na_serial_1 = 5
    Implementação_Futura = 6
    Implementação_Futura = 7
    Cheqsum_da_eprom2_incorreto = 8
    O_equipamento_foi_resetado_rebutado = 9
    # 10 a 15 reservado para aplicacoes especiais



class CodigoDeErro(Enum):
    Start_byte_invalido_stx = 1
    Estrutura_do_pacote_de_comunicacao_invalido = 2
    Estrutura_do_pacote_de_comunicacao_invalido = 3
    Estrutura_do_pacote_de_comunicacao_invalido = 4
    Estrutura_do_pacote_de_comunicacao_invalido = 5
    Estrutura_do_pacote_de_comunicacao_invalido = 6
    Estrutura_do_pacote_de_comunicacao_invalido = 7
    Estrutura_do_pacote_de_comunicacao_invalido = 8
    Estrutura_do_pacote_de_comunicacao_invalido = 9
    Nao_usado = 10
    End_byte_invalido_etx = 11
    Timer_in = 12
    Nao_usado = 13
    Framming = 14
    Over_run = 15
    Buffer_de_recepcao_cheio = 16
    CheqSum = 17
    Buffer_auxiliar_ocupado = 18
    Sequencia_de_byte_enviada_muito_grande = 19



class Tipo(Enum):
    Retorno_Com_Erro = 21
    Retorno_Sem_Erro = 6

class PacoteDeRetornoPadrao(NamedTuple):
    tipo: Tipo
    dadoH: Byte
    dadoL: Byte





if __name__=="__main__":




    pass