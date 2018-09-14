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
notável do formato JSON para chamada de rotinas executadas em servidores na internet, e em [Micro-servicos][micro].

É interessante sempre que possível utilizar o padrão Chave-Valor para representar conjunto de dados em qualquer plataforma,
pois isto também economizará tempo de desenvolvimento. O Python tem em sua biblioteca padrão, ferramentas capazes de
ler e gravar formato JSON e como já dito o [Dict][2] (Dicionário Python) pode fazer várias manipulações neste tipo de
formato.

[1]: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
[2]: https://en.wikipedia.org/wiki/JSON
[RESTFul]: https://en.wikipedia.org/wiki/Representational_state_transfer
[micro]: https://en.wikipedia.org/wiki/Microservices



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

![Exemplo: example_plugin.png](https://github.com/fvilante/cmpppy/blob/develop/CMPP/memmaps/example_plugin.png)


## CMPP MemMap Especificacao


Versao desta especificacao: [0.0.1]

### Modelo de dados

O conceito de *chave-valor* foi aplicado ao conceito de mapa de memoria do CMPP. Portanto um CMPP é visto como um
bloco de memoria que possui chaves *(Parametros CMPP)* e cada chave possui um valor *(Inteiros, Opcoes, etc...
Genericamente chamado: **TypeCast**)*.

Portanto 'Posicao Inicial' é um *Parametro CMPP*, 'Posicao Final' outro e assim por diante.

O formato 'MemMap' define como interpretar um CMPP em termos de Parametros e Valores.

### Especificacao

Nenhum formato que seja invalido em TOML será valido em MemMap. A especificacao valida de formato válido TOML pode
ser consultado [aqui][4] caso necessário. Porém o formato Toml/MemMap é fácil e pode ser utilizado apenas com a
leitura dos próximos parágrafos.

Uma versao da CMPP é chamada genericamente de 'Target', e está diretamente associada com a versao do software em
Assembly do AVR/CMPP. A relação é de um pra um.

Um 'Target' possuirá apenas um arquivo TOML no formato 'MemMap' para o representar. O formato MemMap possui uma
versão que está relacionado com a versão desta especificação que você lê.

Este arquivo possui duas seções: *Header* e *Parameters*, no header temos as informacoes gerais sobre formato e
versão, e em Parameters estão definidos todos os parametros em termos de seus nomes, tipos, posicoes de memoria, etc

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
# etc
# etc...


```


#### [[Parameter]]
Todo parametro começa com esta palavra-chave.

A *identacao* (tabulação no inicio das linhas) não é requisito necessário para a interpretacao do arquivo, porém é recomendável pois facilita leitura humana.

##### Parameter

###### UUID
Esta é a chave-única que especifica o parametro no arquivo. Um erro deverá ser gerado caso exista dois UUID iguais no
mesmo arquivo MemMap.

Este identificador único deverá conter apenas caracteres alfa-numericos [A_Z, a_z, 0_9, '_'] portanto sem acento. A
palavra utilizada aqui será usada para acessar os parametros através da linguagem de programação.

###### Caption
Texto para ser apresentado ao humano que expressa em curtas palavras a intenção do parametro.

###### Doc
Dica de uso do comando.


###### Interface
O conceito de interface é usado para permitir uma mascara de parametros. Onde o driver pode accessar e fazer modificações
apenas aos parametros que pertencem aquela mascara.

Desta forma é possível casos de uso onde uma mesma região de memoria possa ter dois modos de operação distintos.

Por exemplo uma mesma versão AVR/CMPP pode ter dois *modos* de trabalho `Movimentador Generico` e `Dosador de Silicone`:

Interface | Parametro | Posicao de Memoria (Word) | Tamanho da Regiao de Memoria (em bits)
:--|:--|:---:|:--:
`Movimentador Generico` | Posicao Inicial | 80 | 16
`Movimentador Generico` | Posicao Final | 81 | 16
`Movimentador Generico` | Tempo de Start Automatico | 82 | 16

Interface | Parametro | Posicao de Memoria (Word) | Tamanho da Regiao de Memoria (em bits)
:--|:--|:---:|:--:
`Dosador de Silicone` | Posicao Inicial | 80 | 8
`Dosador de Silicone` | Posicao Final | 80 | 8
`Dosador de Silicone` | Velocidade do bico | 82 | 16







###### Tag
Uma TAG é apena uma modo conveniente de filtrar grupos de parametros. Pode-se estabelecer mais de uma tag por parametro.

###### MemRegion
MemRegion é o parametro mais importante, ele indica qual bloco de memoria ontem a informação que queremos.

###### StartWord
Classsicamente chamado de 'Comando' nas versões classicas do protocolo CMPP. Representa o endereço da word que contem
o dado do parametro. Porém mais de uma word pode ser endereçada (veja: BitLength](#bitlength)

O valor é informado no formato decimal.

###### StartBit
Um número entre 0 e 16 que índica dentro da word apontada em [StartWord](#startword) a partir de qual bit comeca o
dado referente ao parametro.

###### BitLength
Um valor inteiro (positivo de 16 bits) que indica quantos bits a partir de StartBit (inclusive) fazem parte do valor
do parametro.

Exemplo:

StartWord | StartBit | BitLen | Comentario
:-:|:-:|:-:|:--
80 | 0 | 16 | Representa uma regiao de memoria de 16 bits que comeca no bit D0 do endereço word 80
80 | 8 | 8 | Regiao de memoria de 8 bits que comeca no bit D8 do endereço word 80
80 | 15 | 1 | Regiao de memoria de 1 bit que comeca no bit D15 do endereço word 80
80 | 3 | 128 | Representa uma regiao de memoria de 128 bits que comeca no bit D3 do endereço word 80

Desta forma [blocos de memoria desalinhados][memalign] e comprimento variavel podem ser especificados.

[memalign]: https://en.wikipedia.org/wiki/Data_structure_alignment#Data_structure_padding

É importante notar que apenas regiões de memoria estão sendo especificadas. Este mecanismo nada fala sobre o conteúdo
ou mesmo formato do dado dentro desta região de memoria. Este papel será efetuado pela chave [TypeCast](#TypeCast)

###### Standard Value
Um valor válido recomendado para o parãmetro caso não exista outro disponível.
A unidade de medida deste valor é `adimensional`. Ele representa um inteiro adimensional que será colocado na
regiao de memoria especificada para o parametro.

###### TypeCast
Existem basicamente 2 TypeCasts disponíveis, outros podem surgir em versões posteriores. A interpretacao do TypeCast
é completamente delegada pela função em run-time que estiver processando o arquivo no momento. Portanto a versão
da função deve ser compativel com a versao de leitura.



### TypeCast

Os formatos de TypeCast são os descritos a seguir: 'Uint16', 'oneOf'

#### Type **Uint16**

Representa *'inteiro positivo de 16 bits'*, com valores máximos e mínimos estabelecidos e usados para validação dos
dados.

Caso valor esteja fora deste range não será enviado para o CMPP, e se for lido não será
considerado um parâmetro válido. Esta informação pode ser útil para compactar os dados em plataformas microcontroladas
por exemplo.

Parametros do Tipo:
* *Value.Min*
* *Value.Max*

Os valores máximos e mínimos podem ser qualquer inteiro positivo entre 0 e 65535 (0xFFFF), e o valor mínimo deve ser
menor do que o valor máximo.

Exemplo:
```toml
    # ...

    [Parameter.TypeCast]
        Type = 'Uint16'
        Value.Min = 0
        Value.Max = 13000

    # ...

```


#### Type **oneOf**

Representa as situacoes onde o parametro é um conjunto de opcoes pré-definidos, por exemplo *ligado*/*desligado*, e
cada opção está mapeada a um inteiro que será representado no mapa de memória.

Parametros do Tipo:
* Array of: { Value, Caption }

Exemplo:
```toml
     # ...

    [Parameter.TypeCast]
        Type = 'oneOf'
        Options = [ { Value = 0, Caption = "Desligado"},
                    { Value = 1, Caption = "Ligado"} ]

     # ...
```


## Outras informacoes

### C++ / AVR

Não há necessidade de especificar este formato para utilizacao em linguagem C++ para microcontroladores, pois um
script python pode ser usado para converter este arquivo em formato MemMap para um arquivo de codigo-fonte C++
contendo estar informacoes de modo compactado ou não, bem como os algoritmos de aceso aos dados.

### ASM / MicroControlador

Poderia-se também criar um script em python para automaticamente ler o arquivo .ASM em assembly e gerar o
arquivo MemMap que o representaria.







