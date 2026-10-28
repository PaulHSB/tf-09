# Os pilares na árvore de arquivos: herança, polimorfismo, abstração e interface.
# Rodar no terminal: python3 pilares.py
#
# O Item da Aula 08 tinha um booleano (eh_pasta) e vários "if eh_pasta".
# Aqui ele vira três classes: Item (o geral), Pasta e Arquivo (os específicos),
# e quem usa a árvore deixa de perguntar "você é pasta?".
from abc import ABC, abstractmethod


# INTERFACE: contrato puro, sem estado e sem implementação.
# Quem assina promete saber dizer o próprio tamanho em bytes.
class Medivel(ABC):
    __slots__ = ()

    @abstractmethod
    def tamanho(self):
        pass


# ABSTRAÇÃO + HERANÇA: o que toda pasta e todo arquivo têm em comum.
# Não dá para criar um Item "solto": ele é só o recorte do essencial.
class Item(Medivel):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__validar_nome(nome)
        self.__nome = nome
        self.__pai = None

        if pai is not None:
            self.mover_para(pai)

    def __validar_nome(self, nome):
        if nome == "" or "/" in nome:
            raise ValueError("nome inválido: " + repr(nome))

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        self.__validar_nome(novo_nome)
        self.__nome = novo_nome

    @property
    def pai(self):
        return self.__pai

    def mover_para(self, destino):
        if destino is self.__pai:
            return

        destino._receber(self)          # cada tipo decide se aceita
        if self.__pai is not None:
            self.__pai._soltar(self)
        self.__pai = destino

    # PROTEGIDO: o gancho que as filhas sobrescrevem. Por padrão, recusa.
    def _receber(self, item):
        raise ValueError(self.__nome + " é um arquivo, não pode conter itens")

    def caminho(self):
        if self.__pai is None:
            return self.__nome
        return self.__pai.caminho() + "/" + self.__nome

    def profundidade(self):
        if self.__pai is None:
            return 0
        return self.__pai.profundidade() + 1

    @abstractmethod
    def mostrar(self):
        pass


class Arquivo(Item):
    __slots__ = ("__bytes",)

    def __init__(self, nome, tamanho_bytes, pai=None):
        if tamanho_bytes < 0:
            raise ValueError("tamanho não pode ser negativo")
        self.__bytes = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        return self.__bytes

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " (" + str(self.tamanho()) + " B)")


class Pasta(Item):
    __slots__ = ("__filhos",)

    def __init__(self, nome, pai=None):
        self.__filhos = []
        super().__init__(nome, pai)

    @property
    def filhos(self):
        return tuple(self.__filhos)

    # OVERRIDE do gancho protegido: a pasta aceita, desde que não crie um ciclo.
    def _receber(self, item):
        ancestral = self
        while ancestral is not None:
            if ancestral is item:
                raise ValueError("não dá para mover " + item.nome + " para dentro dela mesma")
            ancestral = ancestral.pai
        self.__filhos.append(item)

    def _soltar(self, item):
        self.__filhos.remove(item)

    # POLIMORFISMO: a pasta soma o que tem dentro; nenhum filho é perguntado
    # se é pasta ou arquivo, cada um responde do seu jeito.
    def tamanho(self):
        total = 0
        for filho in self.__filhos:
            total = total + filho.tamanho()
        return total

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + "/ (" + str(self.tamanho()) + " B)")
        for filho in self.__filhos:
            filho.mostrar()

# Outra classe que assina o contrato SEM ser da árvore: a Lixeira.
class Lixeira(Medivel):
    __slots__ = ("__descartados",)

    def __init__(self):
        self.__descartados = []

    def descartar(self, arquivo):
        self.__descartados.append(arquivo)

    def tamanho(self):
        total = 0
        for arquivo in self.__descartados:
            total = total + arquivo.tamanho()
        return total


# Quem usa o contrato não sabe (nem quer saber) quem está do outro lado.
def espaco_total(coisas):
    total = 0
    for coisa in coisas:
        total = total + coisa.tamanho()
    return total


def tentar(rotulo, acao):
    try:
        acao()
        print(rotulo, "-> passou (!)")
    except Exception as erro:
        print(rotulo, "->", type(erro).__name__ + ":", erro)

#o Atalho é um Item que só aponta para outro Item.
class Atalho(Item):
    __slots__ = ("__destino",)

    #construtor de atalho, nome e pai sao herdados de Item
    def __init__(self, nome, destino, pai=None):
        super().__init__(nome)
        self.__validar_destino(destino, pai)
        self.__destino = destino

        if pai is not None:
            self.mover_para(pai)

    #getter de destino
    @property
    def destino(self):
        return self.__destino

    #destino é um atributo privado, portanto só é possivel muda-lo atraves desse método
    def redirecionar(self, novo_destino):
        self.__validar_destino(novo_destino, self)
        self.__destino = novo_destino

    # valida se o destino nao esta apontando para ele mesmo subindo pasta por pasta e verificando ate nao ter mais pasta para
    #subir ou o ponto de partida ser igual ao destino.
    def __validar_destino(self, novo_destino, ponto_de_partida):
        ancestral = ponto_de_partida
        while ancestral is not None:
            if ancestral is novo_destino:
                raise ValueError("o atalho " + self.nome + " não pode apontar para si mesmo nem para uma pasta que o contém")
            ancestral = ancestral.pai

    #Aqui entra o polimorfismo, a funcao tamanho mas com uma implementacao diferente
    def tamanho(self):
        return 1

    # Mostra o atalho com o mesmo recuo dos outros itens, apontando para o destino.
    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " -> " + self.__destino.caminho())
        


raiz = Pasta("C:")
usuarios = Pasta("Users", raiz)
usuario = Pasta("peaga", usuarios)
desktop = Pasta("Desktop", usuario)
documentos = Pasta("Documentos", usuario)


trabalho = Arquivo("trabalho.py", 1200, documentos)
foto = Arquivo("foto.png", 3500, desktop)
anotacoes = Arquivo("anotacoes.txt", 300, usuario)


atalho_trabalho = Atalho("trabalho.lnk", trabalho, desktop)
atalho_documentos = Atalho("Documentos.lnk", documentos, desktop)

print("Arvore completa:")
raiz.mostrar()


lixeira = Lixeira()
lixeira.descartar(Arquivo("rascunho.txt", 800))

print()
print("Espaco total (trabalho.py + Desktop + lixeira):", espaco_total([trabalho, desktop, lixeira]), "B")



def mudar_destino_direto():
    atalho_trabalho.destino = anotacoes



def apontar_para_ele_mesmo():
    atalho_trabalho.redirecionar(atalho_trabalho)



def apontar_para_a_propria_pasta():
    atalho_trabalho.redirecionar(desktop)


print()
print("Tentativas que tem que dar erro:")
tentar("mudar atalho.destino direto", mudar_destino_direto)
tentar("atalho apontando para ele mesmo", apontar_para_ele_mesmo)
tentar("atalho apontando para a propria pasta", apontar_para_a_propria_pasta)
