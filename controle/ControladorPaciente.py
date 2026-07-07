from entidade.paciente import Paciente
from limite_gui.TelaPacienteGUI import TelaPacienteGUI
from dao.PacienteDAO import PacienteDAO


class ControladorPaciente:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tela_paciente = TelaPacienteGUI()
        self.__paciente_dao = PacienteDAO()

    def iniciar(self):
        self.abrir_tela()

    def pegar_paciente_por_cpf(self, cpf: str) -> Paciente | None:
        return self.__paciente_dao.get(cpf)

    def selecionar_paciente_para_atendimento(self):
        if len(self.__paciente_dao.get_all()) == 0:
            self.__tela_paciente.mostrar_mensagem("Nenhum paciente cadastrado.")
            return None
        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()
        return self.pegar_paciente_por_cpf(cpf)

    def incluir_paciente(self):
        dados_paciente = self.__tela_paciente.abrir_janela_cadastro()
        if dados_paciente is None:
            return

        paciente_existente = self.pegar_paciente_por_cpf(dados_paciente["cpf"])

        if paciente_existente is not None:
            self.__tela_paciente.mostrar_mensagem("Paciente já cadastrado.")
            return

        novo_paciente = Paciente(
            dados_paciente["nome"],
            dados_paciente["cpf"],
            dados_paciente["celular"],
            dados_paciente["data_nascimento"],
        )

        self.__paciente_dao.add(novo_paciente)
        self.__tela_paciente.mostrar_mensagem("Paciente cadastrado com sucesso!")

    def alterar_paciente(self) -> None:
        if len(self.__paciente_dao.get_all()) == 0:
            self.__tela_paciente.mostrar_mensagem("Nenhum paciente cadastrado.")
            return

        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()
        if cpf is None:
            return
        paciente: Paciente | None = self.pegar_paciente_por_cpf(cpf)

        if paciente is None:
            self.__tela_paciente.mostrar_mensagem("Paciente não encontrado.")
            return
        
        dados_antigos = {
            "nome": paciente.nome,
            "cpf": paciente.cpf,
            "celular": paciente.celular,
            "data_nascimento": paciente.data_nascimento
        }

        novos_dados = self.__tela_paciente.abrir_janela_cadastro(dados_antigos)

        if novos_dados is None:
            return

        # Para não correr o risco de dois pacientes terem o mesmo CPF
        paciente_novo_cpf = self.pegar_paciente_por_cpf(novos_dados["cpf"])

        if paciente_novo_cpf is not None and paciente_novo_cpf != paciente:
            self.__tela_paciente.mostrar_mensagem("Já existe outro paciente com esse CPF.")
            return

        self.__paciente_dao.remove(cpf)

        paciente.nome = novos_dados["nome"]
        paciente.cpf = novos_dados["cpf"]
        paciente.celular = novos_dados["celular"]
        paciente.data_nascimento = novos_dados["data_nascimento"]

        self.__paciente_dao.update(paciente)

        self.__tela_paciente.mostrar_mensagem("Paciente alterado com sucesso.")

    def excluir_paciente(self) -> None:
        if len(self.__paciente_dao.get_all()) == 0:
            self.__tela_paciente.mostrar_mensagem("Nenhum paciente cadastrado.")
            return

        self.listar_pacientes()

        cpf = self.__tela_paciente.selecionar()

        if cpf is None:
            return
        
        paciente = self.pegar_paciente_por_cpf(cpf)

        if paciente is None:
            self.__tela_paciente.mostrar_mensagem("Paciente não encontrado.")
            return

        self.__paciente_dao.remove(cpf)
        self.__tela_paciente.mostrar_mensagem("Paciente removido com sucesso.")

    def listar_pacientes(self) -> None:
        if len(self.__paciente_dao.get_all()) == 0:
            self.__tela_paciente.mostrar_mensagem("Nenhum paciente cadastrado.")
            return

        for paciente in self.__paciente_dao.get_all():
            dados_paciente = {
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "data_nascimento": paciente.data_nascimento,
                "idade": paciente.calcular_idade(),
            }

            self.__tela_paciente.mostrar_paciente(dados_paciente)

    def abrir_tela(self) -> None:
        while True:
            opcao = self.__tela_paciente.mostrar_menu()
            if opcao == "Incluir Paciente":
                self.incluir_paciente()
            
            elif opcao == "Alterar Paciente":
                self.alterar_paciente()
            
            elif opcao == "Excluir Paciente":
                self.excluir_paciente()

            elif opcao == "Listar Pacientes":
                self.listar_pacientes()
            
            elif opcao == "Voltar":
                break

    def voltar(self) -> None:
        return
