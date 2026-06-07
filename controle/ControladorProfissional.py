from limite.TelaProfissional import TelaProfissional
from entidade.profissional import Profissional


class ControladorProfissional:
    def __init__(self, controlador_principal):
        self.__tela_profissional = TelaProfissional(self)
        self.__profissionais = []
        self.__controlador_principal = controlador_principal
    
    def iniciar(self):
        self.abrir_tela()

    def pegar_profissional_por_cpf(self, cpf: str):
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        return None
    
    def selecionar_profissional_para_atendimento(self):
        if len(self.__profissionais) == 0:
            self.__tela_profissional.mostrar_msg("Nenhum profissional cadastrado.")
            return None
        self.listar_profissionais

        cpf = self.__tela_profissional.selecionar()
        return self.pegar_profissional_por_cpf(cpf)
    
    def incluir_profissional(self):
        dados_profissional = self.__tela_profissional.pegar_dados()

        profissional_existente = self.pegar_profissional_por_cpf(dados_profissional["cpf"])

        if profissional_existente is not None:
            self.__tela_profissional.mostrar_msg("Profissional já cadastrado.")
            return

        novo_profissional = Profissional(
            dados_profissional["nome"],
            dados_profissional["cpf"],
            dados_profissional["celular"],
            dados_profissional["especialidade"],
            dados_profissional["registro_profissional"], 
        )

        self.__profissionais.append(novo_profissional)
        self.__tela_profissional.mostrar_msg("Profissional cadastrado com sucesso!")
    
    def alterar_profissional(self) -> None:
        if len(self.__profissionais) == 0:
            self.__tela_profissional.mostrar_msg("Nenhum profissional cadastrado.")
            return

        self.listar_profissionais()

        cpf = self.__tela_profissional.selecionar()
        profissional = self.pegar_profissional_por_cpf(cpf)

        if profissional is None:
            self.__tela_profissional.mostrar_msg("Profissional não encontrado.")
            return

        novos_dados = self.__tela_profissional.pegar_dados()

        # Para não correr o risco de dois profissionais terem o mesmo CPF
        profissional_novo_cpf = self.pegar_profissional_por_cpf(novos_dados["cpf"])

        if profissional_novo_cpf is not None and profissional_novo_cpf != profissional:
            self.__tela_profissional.mostrar_msg("Já existe outro profissional com esse CPF.")
            return

        profissional.nome = novos_dados["nome"]
        profissional.cpf = novos_dados["cpf"]
        profissional.celular = novos_dados["celular"]
        profissional.especialidade = novos_dados["especialidade"]
        profissional.registro_profissional = novos_dados["registro_profissional"]

        self.__tela_profissional.mostrar_msg("Profissional alterado com sucesso.")

    def excluir_profissional(self) -> None:
        if len(self.__profissionais) == 0:
            self.__tela_profissional.mostrar_msg("Nenhum profissional cadastrado.")
            return

        self.listar_profissionais()

        cpf = self.__tela_profissional.selecionar()
        profissional = self.pegar_profissional_por_cpf(cpf)

        if profissional is None:
            self.__tela_profissional.mostrar_msg("Profissional não encontrado.")
            return

        self.__profissionais.remove(profissional)
        self.__tela_profissional.mostrar_msg("Profissional removido com sucesso.")

    def listar_profissionais(self) -> None:
        if len(self.__profissionais) == 0:
            self.__tela_profissional.mostrar_msg("Nenhum profissional cadastrado.")
            return

        for profissional in self.__profissionais:
            dados_profissional = {
                "nome": profissional.nome,
                "cpf": profissional.cpf,
                "celular": profissional.celular,
                "especialidade": profissional.especialidade,
                "registro_profissional": profissional.registro_profissional,
            }

            self.__tela_profissional.mostrar_profissional(dados_profissional)

    def abrir_tela(self) -> None:
        lista_opcoes = {
            1: self.incluir_profissional,
            2: self.alterar_profissional,
            3: self.excluir_profissional,
            4: self.listar_profissionais,
            0: self.voltar,
        }

        continua = True

        while continua:
            opcao_escolhida = self.__tela_profissional.mostrar_menu()

            funcao_escolhida = lista_opcoes[opcao_escolhida]

            if opcao_escolhida == 0:
                continua = False

            funcao_escolhida()

    def voltar(self) -> None:
        return

