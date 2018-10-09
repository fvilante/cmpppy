# CMPP MemMap File-Format


Ultima versao desta especificacao = 0.0.1

NOTA: O ramo Master desta especificacao contém o ultimo desenvolvimento e pode conter funcionalidades que não existe
em versoes anteriores.

## Objetivo


O formato *MemMap* visa especificar as funcionalidades de um sistema CMPP, de forma a poder ser editável em qualquer
editor de textos, e numa semantica que seja obvia. O formato MemMap deve ser iniquivocamente mapeável para um
conjunto de pares [*chave-valor*][3].

[3]: https://en.wikipedia.org/wiki/Attribute%E2%80%93value_pair.


## CMPP MemMap Especificacao


### Modelo de dados

O conceito de *[chave-valor][chave-valor]* foi aplicado ao conceito de mapa de memoria do CMPP. Portanto um CMPP é visto como um
bloco de memoria que possui chaves *(Parametros CMPP)* e cada chave possui um valor *(Inteiros, Opcoes, etc...
Genericamente chamado: **TypeCast**)*.

Portanto 'Posicao Inicial' é um *Parametro CMPP*, 'Posicao Final' outro e assim por diante.

O formato 'MemMap' define como interpretar um CMPP em termos de Parametros e Valores.


[chave-valor]: https://en.wikipedia.org/wiki/Attribute%E2%80%93value_pair


### Especificacao

#### Intro

A especificacao MemMap foi desenhada tendo em vista:
    * Desacoplamento com a [interface de usuario][ui]
    * Genericidade de [casos de uso][uc]

[ui]: https://en.wikipedia.org/wiki/User_interface
[uc]: https://en.wikipedia.org/wiki/Use_case

O formato MemMap é construído em cima do formato TOML[4], que é um formato bem simples de arquivo de configuracao em
estilo texto. Portanto qualquer expressão que seja considerada *invalida* em TOML, também o será em MemMap. Este
documento apresenta como representar um arquivo MemMap valido. O Formato TOML é simples e pode ser consultado
[aqui][4] caso necessario.

#### Detalhamento

Uma versao CMPP é chamada genericamente de 'Target', e está diretamente associada com a versao do software em
Assembly do AVR/CMPP. A relação é de um pra um.

Um 'Target' possuirá apenas um arquivo TOML no formato 'MemMap' para o representar. O formato MemMap possui uma
versão que está relacionado com a versão desta especificação que você lê.

Este arquivo possui duas seções: *Header* e *Parameters*, no header temos as informacoes gerais sobre formato e
versão, e em Parameters estão definidos todos os parametros em termos de seus nomes, tipos, posicoes de memoria, etc

Abaixo um exemplo de arquivo de configuracao, *os comentarios poderão ser omitidos*, as chaves do arquivo TOML (palavras
em inglês) são *case-sensitive* (letras maiusculas ou minusculas são distintas).

Todos os campos são obrigatórios. A tabela TypeCast possui chaves que variam conforme o tipo de dado.

Apesar deste formato apresentar alguns campos que podem ser usados para renderizacao em telas (como o Caption por exemplo),
não é a intenção principal deste formato definir Presentational Layer dos dados a que se refere, e outras camadas
de abstracao devem ser usadas para isto. A principal missao deste formato é representar as funcionalidades de um CMPP
de modo conciso para o programador.

A especificacao MemMap usa o estilo [Camel Case][camel] em suas palavras-chaves.

[camel]: https://en.wikipedia.org/wiki/Camel_case

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


##### UUID
Esta é a chave-única que especifica o parametro no arquivo. Um erro deverá ser gerado caso exista dois UUID iguais no
mesmo arquivo MemMap.

Este identificador único deverá conter apenas caracteres alfa-numericos [A_Z, a_z, 0_9, '_'] portanto sem acento. A
palavra utilizada aqui será usada para acessar os parametros através da linguagem de programação.

##### Caption
Texto para ser apresentado ao humano que expressa em curtas palavras a intenção do parametro.

##### Doc
Dica de uso do comando.


##### Interface
O conceito de interface é usado para permitir uma mascara de parametros. Onde o driver pode accessar e fazer modificações
apenas aos parametros que pertencem aquela mascara.

Desta forma é possível casos de uso onde uma mesma região de memoria possa ter dois modos de operação distintos.

Por exemplo uma mesma versão AVR/CMPP pode ter dois *modos* de trabalho `Movimentador Generico` e `Dosador de Silicone`:

Interface | Parametro | Posicao de Memoria (Word) | Tamanho da Regiao de Memoria (em bits)
:--|:--|:---:|:--:
`Movimentador Generico` | Posicao Inicial | 80 | 16
`Movimentador Generico` | Posicao Final | 81 | 16
`Movimentador Generico` | Tempo de Start Automatico | 82 | 16
`Movimentador Generico` | Largura do sinal de impressao | 82 | 16
`Dosador de Silicone` | Posicao Inicial | 80 | 8
`Dosador de Silicone` | Posicao Final | 80 | 8
`Dosador de Silicone` | Velocidade do bico | 82 | 16

Note que as mesmas regioes de memoria estão sendo apontadas para finalidades distintas. Obviamente espera-se que apenas
uma das duas interfaces sejam usadas de cada vez, e se as duas forem utilizadas numa mesma seção o mecanismo de
orquestração de conflitos ocorre por fora do escopo desta especificacao.

Mais de uma interface pode ser especificada por parametro. Porém uma mesma interface não pode ser especificada duas
vezes.


##### Tag
Uma TAG é apena uma modo conveniente de filtrar grupos de parametros. Pode-se estabelecer mais de uma tag por parametro.
Existem algumas TAGs que são canonicas no CMPP clásico como:

* Parametros de Movimento
* Parametros de Impressao
* Parametros de Ciclo
* Parametros de Impressora

Dentre outros

Esta especificacao não entra no mérito de quais tags devem ou não serem usadas. Porém recomenda-se seguir na medida
do possivel a convenção classica.

##### MemRegion
MemRegion é um dos parametro mais importantes, ele indica qual regiao de memoria contem a informação do parametro.

##### StartWord
Classsicamente chamado de 'Comando' nas versões classicas do protocolo CMPP. Representa o endereço da word que contem
o dado do parametro. Porém mais de uma word pode ser endereçada (veja: BitLength](#bitlength)

O valor é informado no formato decimal.

##### StartBit
Um número entre 0 e 16 que índica dentro da word apontada em [StartWord](#startword) a partir de qual bit comeca o
dado referente ao parametro.

##### BitLength
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

[memalign]: https://en.wikipedia.org/wiki/Data_structure_alignment

É importante notar que apenas regiões de memoria estão sendo especificadas. Este mecanismo nada fala sobre o conteúdo
ou mesmo formato do dado dentro desta região de memoria. Este papel será efetuado pela chave [TypeCast](#TypeCast)

##### Standard Value
Um valor válido recomendado para o parãmetro caso não exista outro disponível.
A unidade de medida deste valor é `adimensional`. Ele representa um inteiro adimensional que será colocado na
regiao de memoria especificada para o parametro.



### TypeCast

Enquanto o MemRegion indica *onde* está o dado, *TypeCast* informa qual é o dado. É através dele que é possível
interpretar o que está dentro da região de memória especificada em *MemRegion*.

Existem basicamente 2 TypeCasts disponíveis 'Uint16', 'OneOf' nesta versão do MemMap.

OBS: A interpretacao do TypeCast é completamente delegada pela função em run-time que estiver processando o arquivo
MemMap no momento. Portanto a versão da peça de software que lê e interpreta o arquivo MemMap, deve estar compatível
com a versão do arquivo MemMap sendo lido.


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


#### Type **OneOf**

Representa as situacoes onde o parametro é um conjunto de opcoes pré-definidos, por exemplo *ligado*/*desligado*, e
cada opção está mapeada a um inteiro que será representado no mapa de memória.

Parametros do Tipo:
* Array of: { Value, Caption }

Esta array não poderá possuir um par Value/Caption
com o mesmo valor. Value é inteiro positivo, e Caption
é qualquer texto.

Exemplo:

```toml
     # ...

    [Parameter.TypeCast]
        Type = 'OneOf'
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

## Sugestoes / Revisões

Este documento esta em versão embrionária, qualquer sugestão de mulhoria é bem vinda. Você pode solicitar revisão
através do 'ISSUE' no github.

Flavio






