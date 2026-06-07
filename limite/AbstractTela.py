from abc import ABC, abstractmethod
from datetime import datetime


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
    
    def le_horario(self, mensagem: str):
        while True:
            try:
                horario_string = input(mensagem)
                return datetime.strptime(horario_string, "%H:%M").time()
            
            except ValueError:
                print("Horário inválido. Digite no formato HH:MM")
    
    def le_float(self, mensagem: str):
        while True:
            try:
                valor = float(input(mensagem))

                if valor >= 0:
                    return valor
                
                print("O valor não pode ser negativo")
            
            except ValueError:
                print("Digite um número válido")

    def le_data(self, mensagem: str):
        while True:
            try:
                data_string = input(mensagem)
                return datetime.strptime(data_string, "%d/%m/%Y").date()
            
            except ValueError:
                print("Data inválida! Digite no formato DD/MM/YYYY")
    
    def le_texto_obrigatorio(self, mensagem: str) -> str:
        while True:
            texto = input(mensagem).strip()

            if texto !="":
                return texto
            print("Esse campo não pode ficar vazio.")
