CMPP MemMap File-Format
========================

Ultima versao desta especificacao = 0.0.1

NOTA: O branch Master desta especificacao contém o ultimo desenvolvimento e pode conter funcionalidades que não existe
em versoes anteriores.

Objetivo
--------

O formato MemMap objetiva especificar as funcionalidades de um sistema CMPP, num formato que seja editável em qualquer
editor de textos ASCII, e numa semantica que seja obvia. O formato MemMap deve ser iniquivocamente mapeável para um
conjunto de pares [chave-valor][3].

[3] https://en.wikipedia.org/wiki/Attribute%E2%80%93value_pair.

### Pares Chave-Valor

Os pares chave valor são altamente reutilizaveis e escalaveis em diversos cenários computacionais. Em Python por exemplo,
um [Dict](1) é um padrão de dado chave-valor. O formato [JSON][2] é um formato muito utilizado por servidores na internet, e
também é baseado no padrão chave-valor. Este padrão de dado pode ser utilizado para importar dados para os
microcontroladores (desde traduzidos do formato texto, para o formato binario).

É interessante sempre que possível utilizar o padrão Chave-Valor para representar conjunto de dados em qualquer plataforma,
pois isto também economizará tempo de desenvolvimento. O Python tem em sua biblioteca padrão, ferramentas capazes de
ler e gravar formato JSON e como já dito o [Dict][2] (Dicionário Python) pode fazer várias manipulações neste tipo de
formato.

[1]: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
[2]: https://en.wikipedia.org/wiki/JSON



TOML
-----

CMPP MemMap format is designed on top of TOML format:

----
"TOML aims to be a minimal configuration file format that's easy to read due to obvious semantics. TOML is designed to map unambiguously to a hash table. TOML should be easy to parse into data structures in a wide variety of languages."
----

For more information about TOML see: https://github.com/toml-lang/toml


CMPP MemMap File-Format
------------------------


