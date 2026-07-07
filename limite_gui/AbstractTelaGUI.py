import FreeSimpleGUI as sg
from abc import ABC, abstractmethod
from datetime import datetime


class AbstractTelaGUI(ABC):
    def __init__(self):
        sg.theme("BluePurple")
    
    @abstractmethod
    def mostrar_menu(self):
        pass
    
    def mostrar_mensagem(self, mensagem):
        sg.popup(mensagem, title="Aviso do Sistema")
    
    def validar_cpf(self, cpf):
            cpf_limpo = cpf.replace(".", "").replace("-", "")
            if cpf_limpo.isdigit() and len(cpf_limpo) == 11:
                return cpf_limpo
            else:
                self.mostrar_mensagem("Digite um CPF válido. Formato de 11 dígitos.")
                return None
    
    def validar_texto(self, texto):
       if texto.strip() != "":
            return texto
       else:
           self.mostrar_mensagem("Esse campo não pode ficar vazio.")
           return None
    
    def validar_celular(self, celular):
            celular_limpo = celular.replace("(", "").replace(")","").replace("-", "").replace(" ", "")
            if celular_limpo.isdigit() and len(celular_limpo) == 11:
                return celular_limpo
            else:
                self.mostrar_mensagem("Digite um celular válido. Formato de 11 dígitos.")
                return None
    
    def validar_data(self, data_texto):
        try:
            data_convertida = datetime.strptime(data_texto, "%d/%m/%Y").date()
            return data_convertida
        except ValueError:
            self.mostrar_mensagem("Data inválida! Digite no formato DD/MM/AAAA")
            return None
    
    def validar_valor(self, valor_texto):
        try:
            valor_limpo = valor_texto.replace(",", ".")
            valor_convertido = float(valor_limpo)
            if valor_convertido >= 0:
                return valor_convertido
            else:
                self.mostrar_mensagem("O valor não pode ser negativo!")
        except ValueError:
            self.mostrar_mensagem("Digite um número válido.")
            return None
    
    def validar_num_inteiro(self, inteiro_texto):
        try:
            inteiro_convertido = int(inteiro_texto)
            if inteiro_convertido >= 0:
                return inteiro_convertido
            else:
                self.mostrar_mensagem("Digite um número positivo.")
        except ValueError:
            self.mostrar_mensagem("Digite um número inteiro válido.")
            return None
    
    def validar_horario(self, horario_texto):
        try:
            horario_convertido = datetime.strptime(horario_texto, "%H:%M").time()
            return horario_convertido
        except ValueError:
            self.mostrar_mensagem("Horário inválido. Digite no formato HH:MM")
            return None
