from abc import ABC, abstractmethod


class AbstractTela(ABC):
    def __init__(self, controlador):
        self._controlador = controlador

    @abstractmethod
    def mostrar_menu(self):
        pass

    def le_num_inteiro(self, mensagem: str, valores_validos: list = None) -> int:
        while True:
            valor_lido = input(mensagem)
            try:
                inteiro = int(valor_lido)

                if valores_validos and inteiro not in valores_validos:
                    raise ValueError

                return inteiro

            except ValueError:
                print("Valor incorreto: Digite um valor numérico inteiro válido.")
                if valores_validos:
                    print("Valores válidos: ", valores_validos)
