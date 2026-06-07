from entidade.paciente import Paciente
from limite.TelaPaciente import TelaPaciente


class ControladorPaciente:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tela_paciente = TelaPaciente(self)
        self.__pacientes = []

    def iniciar(self):
        self.abrir_tela()

    def pegar_paciente_por_cpf(self, cpf: str):
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None
    
    def selecionar_paciente_para_atendimento(self):
        if len(self.__pacientes) == 0:
            self.__tela_paciente.mostrar_msg("Nenhum paciente cadastrado.")
            return None
        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()
        return self.pegar_paciente_por_cpf(cpf)
    

    def incluir_paciente(self):
        dados_paciente = self.__tela_paciente.pegar_dados()

        paciente_existente = self.pegar_paciente_por_cpf(dados_paciente["cpf"])

        if paciente_existente is not None:
            self.__tela_paciente.mostrar_msg("Paciente já cadastrado.")
            return

        novo_paciente = Paciente(
            dados_paciente["nome"],
            dados_paciente["cpf"],
            dados_paciente["celular"],
            dados_paciente["data_nascimento"],
        )

        self.__pacientes.append(novo_paciente)
        self.__tela_paciente.mostrar_msg("Paciente cadastrado com sucesso!")

    def alterar_paciente(self) -> None:
        if len(self.__pacientes) == 0:
            self.__tela_paciente.mostrar_msg("Nenhum paciente cadastrado.")
            return

        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()
        paciente = self.pegar_paciente_por_cpf(cpf)

        if paciente is None:
            self.__tela_paciente.mostrar_msg("Paciente não encontrado.")
            return

        novos_dados = self.__tela_paciente.pegar_dados()

        # Para não correr o risco de dois pacientes terem o mesmo CPF
        paciente_novo_cpf = self.pegar_paciente_por_cpf(novos_dados["cpf"])

        if paciente_novo_cpf is not None and paciente_novo_cpf != paciente:
            self.__tela_paciente.mostrar_msg("Já existe outro paciente com esse CPF.")
            return

        paciente.nome = novos_dados["nome"]
        paciente.cpf = novos_dados["cpf"]
        paciente.celular = novos_dados["celular"]
        paciente.data_nascimento = novos_dados["data_nascimento"]

        self.__tela_paciente.mostrar_msg("Paciente alterado com sucesso.")

    def excluir_paciente(self) -> None:
        if len(self.__pacientes) == 0:
            self.__tela_paciente.mostrar_msg("Nenhum paciente cadastrado.")
            return

        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()
        paciente = self.pegar_paciente_por_cpf(cpf)

        if paciente is None:
            self.__tela_paciente.mostrar_msg("Paciente não encontrado.")
            return

        self.__pacientes.remove(paciente)
        self.__tela_paciente.mostrar_msg("Paciente removido com sucesso.")

    def listar_pacientes(self) -> None:
        if len(self.__pacientes) == 0:
            self.__tela_paciente.mostrar_msg("Nenhum paciente cadastrado.")
            return

        for paciente in self.__pacientes:
            dados_paciente = {
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "data_nascimento": paciente.data_nascimento,
                "idade": paciente.calcular_idade(),
            }

            self.__tela_paciente.mostrar_paciente(dados_paciente)

    def abrir_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_paciente,
            2: self.alterar_paciente,
            3: self.excluir_paciente,
            4: self.listar_pacientes,
            0: self.voltar,
        }

        continua = True

        while continua:
            opcao_escolhida = self.__tela_paciente.mostrar_menu()

            funcao_escolhida = lista_opcoes[opcao_escolhida]

            if opcao_escolhida == 0:
                continua = False

            funcao_escolhida()

    def voltar(self) -> None:
        return
