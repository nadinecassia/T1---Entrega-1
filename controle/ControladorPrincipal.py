from limite.TelaPrincipal import TelaPrincipal

from controle.ControladorAtendimento import ControladorAtendimento
from controle.ControladorClinica import ControladorClinica
from controle.ControladorPaciente import ControladorPaciente
from controle.ControladorPagamento import ControladorPagamento
from controle.ControladorProcedimento import ControladorProcedimento
from controle.ControladorProfissional import ControladorProfissional
from controle.ControladorRelatorio import ControladorRelatorio
from controle.ControladorTipoAtendimento import ControladorTipoAtendimento


class ControladorPrincipal:
    def __init__(self) -> None:
        self.__tela_principal = TelaPrincipal(self)

        self.__controlador_clinica = ControladorClinica(self)
        self.__controlador_paciente = ControladorPaciente(self)
        self.__controlador_profissional = ControladorProfissional(self)
        self.__controlador_tipo_atendimento = ControladorTipoAtendimento(self)
        self.__controlador_procedimento = ControladorProcedimento(self)
        self.__controlador_atendimento = ControladorAtendimento(self)
        self.__controlador_pagamento = ControladorPagamento(self)
        self.__controlador_relatorio = ControladorRelatorio(self)

    @property
    def controlador_clinica(self):
        return self.__controlador_clinica

    @property
    def controlador_paciente(self):
        return self.__controlador_paciente

    @property
    def controlador_profissional(self):
        return self.__controlador_profissional

    @property
    def controlador_tipo_atendimento(self):
        return self.__controlador_tipo_atendimento

    @property
    def controlador_procedimento(self):
        return self.__controlador_procedimento

    @property
    def controlador_atendimento(self):
        return self.__controlador_atendimento

    @property
    def controlador_pagamento(self):
        return self.__controlador_pagamento

    @property
    def controlador_relatorio(self):
        return self.__controlador_relatorio

    def iniciar(self) -> None:
        self.abrir_tela()

    def abrir_tela(self) -> None:
        lista_opcoes = {
            1: self.__controlador_clinica.abrir_tela,
            2: self.__controlador_paciente.abrir_tela,
            3: self.__controlador_profissional.abrir_tela,
            4: self.__controlador_tipo_atendimento.abrir_tela,
            5: self.__controlador_procedimento.abrir_tela,
            6: self.__controlador_atendimento.abrir_tela,
            7: self.__controlador_pagamento.abrir_tela,
            8: self.__controlador_relatorio.abrir_tela,
            0: self.encerrar_sistema,
        }

        continua = True

        while continua:
            opcao_escolhida = self.__tela_principal.mostrar_menu()

            if opcao_escolhida == 0:
                continua = False
                self.encerrar_sistema()
            else:
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida()

    def encerrar_sistema(self) -> None:
        print("Sistema encerrado.")
