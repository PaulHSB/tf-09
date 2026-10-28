## Encapsulamento
Encapsulamento é você "fechar" a classe impedindo que alguém de fora à modifique. Você proteje os objetos. O atributo destino é privado, única maneira de mudá-lo é usando o método redirecionar.

## Herança
É quando uma classe recebe tudo o que tem da sua classe mãe, se a classe *A* tem x atributos e y métodos, a classe *B*, caso herde de *A*, também tera x atributos e y métodos + os atributos e métodos específicos dela. A classe atalho herda de Item, por isso ela já sabe o que é nome e pai, o atributo exclusivo de Atalho é destino.

## Polimosfismo
No porlimorfismo, nós chamamos a mesma função, ela é executada em objetos diferentes, usando lógicas diferentes no corpo da função, mas produzindo o mesmo resultado. A herança da classe mãe não é tão rígida. O que importa é o output gerado, como o tamanho de um arquivo ou pasta. O cáculo do tamanho é diferente para cada tipo de arquivo, em atalho está programado para sempre retornar 1.

## Interface
É uma classe de métodos vazios, por que ela não se importa como você irá fazer, o importante é que você faça caso use seu método.

## Implementação
É como a coisa funciona por dentro. A interfaça se importa com o que é usado, a implementeção disso (o como) não interessa