from limite_gui.TelaProfissionalGUI import TelaProfissionalGUI
from entidade.profissional import Profissional
from dao.ProfissionalDAO import ProfissionalDAO


class ControladorProfissional:
    def __init__(self, controlador_principal):
        self.__tela_profissional = TelaProfissionalGUI(self)
        self.__profissional_dao = ProfissionalDAO()
        self.__controlador_principal = controlador_principal

    def iniciar(self):
        self.abrir_tela()

    def pegar_profissional_por_cpf(self, cpf: str) -> Profissional | None:
        return self.__profissional_dao.get(cpf)

    def selecionar_profissional_para_atendimento(self):
        profissionais = self.__profissional_dao.get_all()
        
        if len(profissionais) == 0:
            self.__tela_profissional.mostrar_mensagem("Nenhum profissional cadastrado.")
            return None

        cpf = self.__tela_profissional.tabela_profissionais(
            profissionais,
            selecionar=True
        )

        if cpf is None:
            return None

        if cpf < 0 or cpf >= len(profissionais):
            self.__tela_profissional.mostrar_mensagem("Profissional não encontrado.")
            return None
        
        return profissionais[cpf]
    

    def selecionar_profissional_para_procedimento(self):
        return self.selecionar_profissional_para_atendimento()

    def incluir_profissional(self):
        dados_profissional = self.__tela_profissional.abrir_janela_cadastro()
        if dados_profissional is None:
            return
        
        profissional_existente = self.pegar_profissional_por_cpf(
            dados_profissional["cpf"]
        )

        if profissional_existente is not None:
            self.__tela_profissional.mostrar_mensagem("Profissional já cadastrado.")
            return

        novo_profissional = Profissional(
            dados_profissional["nome"],
            dados_profissional["cpf"],
            dados_profissional["celular"],
            dados_profissional["especialidade"],
            dados_profissional["registro_profissional"],
        )

        self.__profissional_dao.add(novo_profissional)
        self.__tela_profissional.mostrar_mensagem("Profissional cadastrado com sucesso!")

    def alterar_profissional(self) -> None:
        if len(self.__profissional_dao.get_all()) == 0:
            self.__tela_profissional.mostrar_mensagem("Nenhum profissional cadastrado.")
            return

        cpf = self.__tela_profissional.tabela_profissionais(
            self.__profissional_dao.get_all(),
            selecionar=True
        )

        if cpf is None:
            return
        
        profissional = self.pegar_profissional_por_cpf(cpf)

        if profissional is None:
            self.__tela_profissional.mostrar_mensagem("Profissional não encontrado.")
            return
        
        dados_antigos = {
            "nome": profissional.nome,
            "cpf": profissional.cpf,
            "celular": profissional.celular,
            "especialidade": profissional.especialidade,
            "registro_profissional": profissional.registro_profissional
        }

        novos_dados = self.__tela_profissional.abrir_janela_cadastro(dados_antigos)

        if novos_dados is None:
            return
        
        # Para não correr o risco de dois profissionais terem o mesmo CPF
        profissional_novo_cpf = self.pegar_profissional_por_cpf(novos_dados["cpf"])

        if profissional_novo_cpf is not None and profissional_novo_cpf != profissional:
            self.__tela_profissional.mostrar_mensagem(
                "Já existe outro profissional com esse CPF."
            )
            return

        self.__profissional_dao.remove(cpf)

        profissional.nome = novos_dados["nome"]
        profissional.cpf = novos_dados["cpf"]
        profissional.celular = novos_dados["celular"]
        profissional.especialidade = novos_dados["especialidade"]
        profissional.registro_profissional = novos_dados["registro_profissional"]

        self.__profissional_dao.update(profissional)
        self.__tela_profissional.mostrar_mensagem("Profissional alterado com sucesso.")

    def excluir_profissional(self) -> None:
        if len(self.__profissional_dao.get_all()) == 0:
            self.__tela_profissional.mostrar_mensagem("Nenhum profissional cadastrado.")
            return

        cpf = self.__tela_profissional.tabela_profissionais(
            self.__profissional_dao.get_all(),
            selecionar=True
        )

        if cpf is None:
            return
        
        profissional = self.pegar_profissional_por_cpf(cpf)

        if profissional is None:
            self.__tela_profissional.mostrar_mensagem("Profissional não encontrado.")
            return

        self.__profissional_dao.remove(cpf)
        self.__tela_profissional.mostrar_mensagem("Profissional removido com sucesso.")

    def listar_profissionais(self) -> None:
        profissionais = self.__profissional_dao.get_all()

        if len(profissionais) == 0:
            self.__tela_profissional.mostrar_mensagem("Nenhum profissional cadastrado.")
            return
        
        self.__tela_profissional.tabela_profissionais(profissionais)

    def abrir_tela(self) -> None:
        while True:
            opcao = self.__tela_profissional.mostrar_menu()
            if opcao == "Incluir Profissional":
                self.incluir_profissional()

            elif opcao == "Alterar Profissional":
                self.alterar_profissional()

            elif opcao == "Excluir Profissional":
                self.excluir_profissional()

            elif opcao == "Listar Profissionais":
                self.listar_profissionais()

            elif opcao == "Voltar":
                break

    def voltar(self) -> None:
        return
