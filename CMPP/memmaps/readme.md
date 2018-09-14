# CMPP MemMap File-Format


Ultima versao desta especificacao = 0.0.1

NOTA: O ramo Master desta especificacao contém o ultimo desenvolvimento e pode conter funcionalidades que não existe
em versoes anteriores.

## Objetivo


O formato *MemMap* visa especificar as funcionalidades de um sistema CMPP, de forma a poder ser editável em qualquer
editor de textos, e numa semantica que seja obvia. O formato MemMap deve ser iniquivocamente mapeável para um
conjunto de pares [*chave-valor*][3].

[3]: https://en.wikipedia.org/wiki/Attribute%E2%80%93value_pair.


## Introdução

O texto introdutorio a seguir apresenta alguamas questões sobre o design do formato, caso queira pode pular direto para
a [Especificacao](#cmpp-memmap-especificacao)


### Pares *Chave-Valor*

Os pares chave valor são altamente reutilizaveis e escalaveis em diversos cenários computacionais. Em Python por exemplo,
um [Dict][1] é um padrão de dado chave-valor. O formato [JSON][2] é um formato muito utilizado por servidores na internet, e
também é baseado no padrão chave-valor. Este padrão de dado pode ser utilizado para importar dados para os
microcontroladores (desde traduzidos do formato texto, para o formato binario). Servidores [RESTFul][RESTFul] é uma aplicação
notável do formato JSON para chamada de funções de programação que são servidas pela internet.

É interessante sempre que possível utilizar o padrão Chave-Valor para representar conjunto de dados em qualquer plataforma,
pois isto também economizará tempo de desenvolvimento. O Python tem em sua biblioteca padrão, ferramentas capazes de
ler e gravar formato JSON e como já dito o [Dict][2] (Dicionário Python) pode fazer várias manipulações neste tipo de
formato.

[1]: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
[2]: https://en.wikipedia.org/wiki/JSON
[RESTFul]: https://en.wikipedia.org/wiki/Representational_state_transfer



### Formato TOML


[O formato TOML][4] foi escolhido por além dele atender os requisitos apresentados acima, ele tem como foco a facilidade
semantica em que apresenta as informacoes. Ele é muito parecido com o antigo [formato .INI][5] de configuracao do Windows,
porém mais poderoso por permitir maior nível de 'aninhamento' de dados *('nesting' em ingles)*.


Os objetivos do formato oficialmente são definidos como:
```
"TOML aims to be a minimal configuration file format that's easy to read due to obvious semantics. TOML is designed
to map unambiguously to a hash table. TOML should be easy to parse into data structures in a wide variety of languages."
```

[4]: https://github.com/toml-lang/toml/tree/v0.5.0#user-content-table
[5]: https://en.wikipedia.org/wiki/INI_file

```
*OBS: Outros formatos como o .CSV, .XLS, .DB foram avaliados, porém este dado possui uma característica polimórfica no
campo *TypeCast* (o tipo de dado que ele especifica pode variar) e portanto é mais difícil de expressar nestes formatos
do que em TOML, além de este último não exigir ferramentas adicionais além de um editor de textos, o que facilita
manuseio em campo.
```

O ponto contra ao formato TOML é que ele por ser mais recente não é tão popular quanto o formato JSON (que possui
inclusive boas ferramentas on-line para edição) e possui muitos blogs em português o detalhando. Porém os bibliotecas
TOML foram consideradas maduras o suficiente para a tarefa exigida, e a facilidade de uso dispensaria consultas em
português. Além disto é possível converter de TOML para JSON e vice-versa com facilidade. Alem disto
uma cópia deste arquivo de instrucoes pode ser deixada junto com os drivers MemMap (ou até dentro dele como comentário)
para fácil consulta.


#### Versao

A versão do TOML escolhida é a última disponível no momento, que a [v.0.5.0][6]

A especificacao TOML possui implementacoes em codigo aberto no github em python, C++ e outras linguagens. De todos
os drivers disponíveis foi adotado o [TOMLKIT][7] por apresentar excelente flexibilidade e compatibilidade com a
versao TOML escolhida.

[6]: https://github.com/toml-lang/toml/blob/master/versions/en/toml-v0.5.0.md
[7]: https://github.com/sdispater/tomlkit

#### Plugins

É possível encontrar plugins para edição do formato TOML para IDE's de edicao de codigo-fonte, como por exemplo o
[PyCharm](https://www.jetbrains.com/pycharm/).

![](.example_plugin.jpg)


## CMPP MemMap Especificacao


Versao desta especificacao: [0.0.1]

### Modelo de dados

O conceito de *chave-valor* foi aplicado ao conceito de mapa de memoria do CMPP. Portanto um CMPP é visto como um
bloco de memoria que possui chaves *(Parametros CMPP)* e cada chave possui um valor *(Inteiros, Opcoes, etc...
Genericamente chamado: **TypeCast**)*.

Portanto 'Posicao Inicial' é um *Parametro CMPP*, 'Posicao Final' outro e assim por diante.

O formato 'MemMap' define como interpretar um CMPP em termos de Parametros e Valores.

### Especificacao

Uma versao CMPP é chamada genericamente de 'Target', e está diretamente associada com a versao do software em Assembly
que está no CMPP.

Um 'Target' possuirá apenas um arquivo TOML no formato 'MemMap' para o representar.

Este arquivo possui duas seções: *Header* e *Parameters*, no header temos as informacoes gerais sobre o formato e
versoes, e em Parameters estão definidos todos os parametros em termos de seus nomes, tipos, posicoes de memoria e
comprimentos de dados no CMPP, etc.

Abaixo um exemplo de arquivo de configuracao, *os comentarios poderão ser omitidos*, as chaves do arquivo TOML (palavras
em inglês) são *case-sensitive* (letras maiusculas ou minusculas são distintas):

```toml
title = "Memmap do driver CMPP00LG"  # Qualquer informacao pode estar no título

[Header]
    File.Format.Type = "CMPPMemMapFile"  # Formato deste arquivo de texto
    File.Format.Version = [0,0,1]        # Versao desta especificacao
    Driver.Revision = [0,0,1]            # Revisao deste driver em relacao ao software CMPP
    Driver.Target = "CMPP00LG"           # Qual versao do AVR este driver especifica


[[Parameter]]
    [Parameter.Description]
        UUID = "Posicao_inicial"
        Caption = "Posicao inicial"
        Doc = "Posicao inicial do movimento, normalmente mais proxima ao motor"
    [Parameter.MetaData]
        Interface = ['Movimentador Generico']
        Tag = ['Parametros de Movimento']
    [Parameter.MemRegion]
        StartWord = 80
        StartBit = 0
        BitLength = 16
    [Parameter.Default]
        Value = 10
    [Parameter.TypeCast]
        Type = 'Uint16'
        Value.Min = 0
        Value.Max = 13000

[[Parameter]]
    [Parameter.Description]
        UUID = "Posicao_final"
        Caption = "Posicao final"
        Doc = "Posicao final do movimento, normalmente mais afastada ao motor"
    [Parameter.MetaData]
        Interface = ['Movimentador Generico']
        Tag = ['Parametros de Movimento']
    [Parameter.MemRegion]
        StartWord = 81
        StartBit = 0
        BitLength = 16
    [Parameter.Default]
        Value = 100
    [Parameter.TypeCast]
        Type = 'Uint16'
        Value.Min = 0
        Value.Max = 13000

# Adicionar mais quantos parametros forem necessários...


```


#### [[Parameter]]
Todo parametro começa com esta chave

##### Parameter
* *UUID*: Esta é a chave única deste parametro, não pode conter outro igual no arquivo. É destinado a ser usado dentro da
linguagem de programação pelo programador não deverá conter espaços, acentos ou caracteres especiais.
* *Caption*: Texto para ser apresentado ao cliente/humano.
* *Doc*: Dica de uso do comando.
* *Interface*: Define um modo de acesso aos parametros. Permite que varios parametros possam usar uma mesma posicao de
memória. Pode haver mais de um por parametro.
* *Tag*: Uma TAG é apena uma modo conveniente de filtrar grupos de parametros. Pode-se estabelecer mais de uma tag por parametro.
* *MemRegion*: MemRegion é o parametro mais importante, ele indica qual bloco de memoria ontem a informação que queremos.
* *StartWord*: Classsicamente chamado de 'Comando' nas versões classicas do protocolo CMPP.
* *StartBit*: Uma vez localizada a 'word' em qual bit começa a informação que queremos.
* *BitLength*: A partir do 'StartBit' quantos bits é o comprimento da nossa informação.
* *Value*: Um valor válido recomendado para o parãmetro caso não exista outro disponível.
* *TypeCast* Existem basicamente 2 TypeCasts disponíveis, e eles podem ser extendidos em versões posteriores.
* *Type*:
** 'Uint16' :Neste caso usamos um 'Inteiro positivo de 16 bits'
*** Value.Min: Mínimo valor aceitável
*** Value.Max: Máximo. Caso valor esteja fora deste range não será enviado para o CMPP, e se for lido não será
considerado um parâmetro válido. Esta informação pode ser útil para compactar os dados em plataformas microcontroladas

### TypeCast

Os formatos de TypeCast são os descritos a seguir: 'Uint16', 'oneOf' [detalhar mais esta parte]


### C++ / AVR

Não há necessidade de especificar este formato para utilizacao em linguagem C++ para microcontroladores, pois um
script python pode ser usado para converter este arquivo em formato MemMap para um arquivo de codigo-fonte C++
contendo estar informacoes de modo compactado ou não, bem como os algoritmos de aceso aos dados.

### ASM / MicroControlador

Poderia-se também criar um script em python para automaticamente ler o arquivo .ASM em assembly e gerar o
arquivo MemMap que o representaria.







