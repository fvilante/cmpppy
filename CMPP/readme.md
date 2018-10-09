### Pares *Chave-Valor*

Os pares [chave valor][chave-valor] são altamente reutilizaveis e escalaveis em diversos cenários computacionais. Em Python por exemplo,
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
[chave-valor]: https://en.wikipedia.org/wiki/Attribute%E2%80%93value_pair


### Formato TOML


O [formato TOML][4] foi escolhido por além dele atender os requisitos apresentados acima, ele tem como foco a facilidade
semantica em que apresenta as informacoes. Ele é muito parecido com o [formato .INI][5] utilizado por versoes anteriores
do Windows porém é mais poderoso na medida em que permite o '[aninhamento][nesting]' da estrutura de dados.

[nesting]: https://en.wikipedia.org/wiki/Nesting_(computing)#Data_Structures

O formato TOML tem o seguinte objetivo declarado:
```
"TOML aims to be a minimal configuration file format that's easy to read due to obvious semantics.
TOML is designed to map unambiguously to a hash table. TOML should be easy to parse into data structures
in a wide variety of languages."
```

[4]: https://github.com/toml-lang/toml/tree/v0.5.0#toml
[5]: https://en.wikipedia.org/wiki/INI_file


*OBS*: Outros formatos como o .CSV, .XLS, .DB foram avaliados, porém este dado possui uma característica
[polimórfica][polimorphism] no campo [*TypeCast*](#typecast) (o tipo de dado que ele especifica pode variar) e portanto é mais
difícil de expressar nestes formatos do que em TOML, além de este último não exigir ferramentas adicionais além de
um editor de textos, o que facilita manuseio em campo.

[polimorphism]: https://en.wikipedia.org/wiki/Subtyping

O ponto contra ao formato TOML é que ele por ser mais recente não é tão popular quanto o formato JSON (que possui
inclusive boas ferramentas on-line para edição) e possui muitos blogs em português o detalhando. Porém os bibliotecas
TOML foram consideradas maduras o suficiente para a tarefa exigida, e a facilidade de uso dispensaria consultas em
português. Além disto é possível converter de TOML para JSON e vice-versa com facilidade. Alem disto
uma cópia deste arquivo de instrucoes pode ser deixada junto com os drivers MemMap (ou até dentro dele como comentário)
para fácil consulta.


#### Versao

A versão do TOML escolhida é a última disponível no momento, que a [v.0.5.0][6]

A especificacao TOML possui implementacoes em codigo aberto no github em python, C++ e outras linguagens. De todos
os drivers disponíveis foi adotado o [TOMLKIT][7] por apresentar boa flexibilidade e compatibilidade com a
versao TOML escolhida.

[6]: https://github.com/toml-lang/toml/blob/master/versions/en/toml-v0.5.0.md
[7]: https://github.com/sdispater/tomlkit

#### Plugins

É possível encontrar plugins para edição do formato TOML para IDE's de edicao de codigo-fonte, como por exemplo o
[PyCharm](https://www.jetbrains.com/pycharm/).

![Exemplo: example_plugin.png](https://github.com/fvilante/cmpppy/blob/develop/CMPP/memmaps/example_plugin.png)
