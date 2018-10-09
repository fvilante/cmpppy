# CMPP Pos File-Format


Ultima versao desta especificacao = 0.0.1

NOTA: O ramo Master desta especificacao contém o ultimo desenvolvimento e pode conter funcionalidades que não existe
em versoes anteriores.

## Objetivo


Este formato armazena *programas* CMPPs. Ele engloba apenas parâmetros que podem ser enviados ou lidos do CMPP.

Os detalhes de *como* fazer o acesso do parametro no CMPP é descrito por outro formato, o [Formato CMPP MemMap][1]


[1]:https://github.com/fvilante/cmpppy/blob/develop/CMPP/memmaps/readme.md


## Formato

### Arquivo TOML

Cada arquivo toml, pode conter vários programas 'POS'.
O arquivo toml é dividido em Header e Tabela de Programas POS.

#### Header

O Header contem informaçoes gerais sobre o arquivo TOML, como assinatura do formato de arquivo
e versão do formato, dentre outras. Estas informações são uteis por exemplo para que o parser
do arquivo seja capaz de utilizar o correto algoritmo de interpretação para ler o arquivo.

#### Tabela de Programas POS

Cada tabela armazena um conjunto de parametros CMPP. O valor do parametro e uma referencia para
o Driver MemMap que deve ser usado para interpretar o parametro.

Um programa POS é dividido em 2 seccoes: Header e Body

##### Header

Aqui é indicado o driver MemMap que deve ser usado para interpretar o programa POS.

##### Body

Os parametros e seus respectivos valores. Os 'parametros' devem corresponder ao UUID do
parametro que está indicado do Driver MemMap respectivo. E lembre-se que os valores
apontados devem estar dentro do intervalo válido no Driver MemMap. Um valor não valido
irá gerar um erro de run-time durante o carregamento.



## Sugestoes / Revisões

Este documento esta em versão embrionária, qualquer sugestão de melhoria é bem vinda. Você pode solicitar revisão
através do 'ISSUE' no github.

Flavio






