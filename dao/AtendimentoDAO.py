from dao.DAO import DAO
from entidade.atendimento import Atendimento
from datetime import date


class AtendimentoDAO(DAO):
    def __init__(self):
        super().__init__('atendimentos.pkl')

    def __cria_chave(self, cpf: str, data: date):
        return f"{cpf}_{data.strftime('%Y-%m-%d')}"

    def add(self, atendimento: Atendimento):
        if (isinstance(atendimento, Atendimento) and 
            isinstance(atendimento.paciente.cpf, str) and 
            isinstance(atendimento.data, date)):
            
            chave = self.__cria_chave(atendimento.paciente.cpf, atendimento.data)
            super().add(chave, atendimento)

    def update(self, atendimento: Atendimento):
        if (isinstance(atendimento, Atendimento) and 
            isinstance(atendimento.paciente.cpf, str) and 
            isinstance(atendimento.data, date)):
            
            chave = self.__cria_chave(atendimento.paciente.cpf, atendimento.data)
            super().update(chave, atendimento)

    def get(self, cpf: str, data: date):
        if isinstance(cpf, str) and isinstance(data, date):
            chave = self.__cria_chave(cpf, data)
            return super().get(chave)
        return None

    def remove(self, cpf: str, data: date):
        if isinstance(cpf, str) and isinstance(data, date):
            chave = self.__cria_chave(cpf, data)
            super().remove(chave)
