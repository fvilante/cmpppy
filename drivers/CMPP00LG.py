from enum import Enum, auto


class Enum_AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class CmppEnumInterface(Enum_AutoName):
    pass

# Enum na intencao de uniformizar os rotulos de texto, e dar a possibilidade
# deles serem auto-listados pela IDE
class Movimentador_Generico(CmppEnumInterface):
    # arquivo de eixo(apenas referente a placa CMPP)
    Posicao_inicial = auto()
    Posicao_final = auto()
    Aceleracao_de_avanco = auto()
    Aceleracao_de_retorno = auto()
    Velocidade_de_avanco = auto()
    Velocidade_de_retorno = auto()
    Numero_de_mensagens_no_avanco = auto()
    Numero_de_mensagens_no_retorno = auto()
    Posicao_da_primeira_impressao_no_avanco = auto()
    Posicao_da_primeira_impressao_no_retorno = auto()
    Posicao_da_ultima_impressao_no_avanco = auto()
    Posicao_da_ultima_impressao_no_retorno = auto()
    Largura_do_sinal_de_impressao = auto()
    Tempo_para_start_automatico = auto()
    Tempo_para_start_externo = auto()
    Antecipacao_da_saida_de_start = auto()
    # configuracao de eixo(apenas referente a placa CMPP)
    Janela_de_protecao_para_o_giro = auto()
    Numero_de_pulsos_por_giro_do_motor = auto()
    Valor_da_posicao_de_referencia = auto()
    Aceleracao_de_referencia = auto()
    Velocidade_de_referencia = auto()
    # CMDFLASH = 96(0x60)
    Start_automatico_no_avanco = auto()
    Start_automatico_no_retorno = auto()
    Saida_de_start_no_avanco = auto()
    Saida_de_start_no_retorno = auto()
    Entrada_de_start_externo = auto()
    Logica_de_start_externo = auto()
    Entrada_de_start_entre_eixos = auto()
    Referencia_pelo_start_externo = auto()
    Logica_de_sinal_de_impressao = auto()
    Logica_de_sinal_de_reversao = auto()
    Selecao_de_mensagem_via_serial = auto()
    Reversao_de_mensagem_via_serial = auto()
    Giro_com_funcao_de_protecao = auto()
    Giro_com_funcao_de_correcao = auto()
    Reducao_da_corrente_de_repouso = auto()
    Modo_continuo_passo_a_passo = auto()


