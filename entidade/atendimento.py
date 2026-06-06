from datetime import date, time
from entidade.clinica import Clinica
from entidade.paciente import Paciente
from entidade.profissional import Profissional
from entidade.procedimento import Procedimento
from entidade.pagamento import Pagamento
from entidade.TipoAtendimento import TipoAtendimento


class Atendimento:
    def __init__(
        self,
        data: date,
        horario_inicio: time,
        horario_fim: time,
        tipo_atendimento: TipoAtendimento,
        valor: float,
        clinica: Clinica,
        paciente: Paciente,
        profissional: Profissional,
    ):
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo_atendimento = tipo_atendimento
        self.__valor = valor

        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional

        self.__procedimentos = []
        self.__pagamentos = []

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def horario_inicio(self):
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio):
        self.__horario_inicio = horario_inicio

    @property
    def horario_fim(self):
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, horario_fim):
        self.__horario_fim = horario_fim

    @property
    def tipo_atendimento(self):
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento):
        self.__tipo_atendimento = tipo_atendimento

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = valor

    @property
    def clinica(self):
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica):
        self.__clinica = clinica

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente):
        self.__paciente = paciente

    @property
    def profissional(self):
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional):
        self.__profissional = profissional

    def add_procedimento(self, procedimento: Procedimento):
        self.__procedimentos.append(procedimento)

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    def add_pagamentos(self, pagamento: Pagamento):
        self.__pagamentos.append(pagamento)

    @property
    def pagamentos(self) -> list:
        return self.__pagamentos

    def calcular_valor_restante(self) -> float:
        valor_restante = self.__valor

        for pagamento in self.__pagamentos:
            valor_restante -= pagamento.valor_pago

        return valor_restante

    def calcular_custo_total_procedimentos(self) -> float:
        total_procedimentos = 0

        for procedimento in self.__procedimentos:
            total_procedimentos += procedimento.custo

        return total_procedimentos

    def horario_valido(self) -> bool:
        return self.__clinica.esta_aberta(self.__horario_inicio, self.__horario_fim)
