class TipoAtendimento:
    def __init__(self, nome: str, descricao: str) -> None:
        self.__nome = nome
        self.__descricao = descricao

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def descricao(self) -> str:
        return self.__descricao

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        self.__descricao = descricao
