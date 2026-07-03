class TipoAtendimento:
    def __init__(self,codigo: int, nome: str, descricao: str) -> None:
        self.__codigo = codigo
        self.__nome = nome
        self.__descricao = descricao

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def descricao(self) -> str:
        return self.__descricao
    
    @property
    def codigo(self) -> int:
        return self.__codigo

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        self.__descricao = descricao
    
    @codigo.setter
    def codigo(self, codigo: int) -> None:
        self.__codigo = codigo
