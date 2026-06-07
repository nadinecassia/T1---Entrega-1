from entidade.procedimento import Procedimento
from limite.TelaProcedimento import TelaProcedimento


class ControladorProcedimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__procedimentos = []
        self.__tela_procedimento = TelaProcedimento(self)

    @property
    def procedimentos(self):
        return self.__procedimentos

    def iniciar(self):
        self.abrir_tela()

    def selecionar_procedimento_para_atendimento(self):
        if len(self.__procedimentos) == 0:
            self.__tela_procedimento.mostrar_msg("Nenhum procedimento cadastrado no sistema!")
            return None

        self.listar_procedimentos()

        descricao_busca = self.__tela_procedimento.selecionar()

        for proc in self.__procedimentos:
            if proc.descricao.lower() == descricao_busca.lower():
                return proc

        self.__tela_procedimento.mostrar_msg("ERRO: Procedimento com a descrição informada não foi localizado.")
        return None

    def incluir_procedimento(self):
        dados_proc = self.__tela_procedimento.pegar_dados()

        for proc in self.__procedimentos:
            if proc.descricao.lower() == dados_proc["descricao"].lower():
                self.__tela_procedimento.mostrar_msg(
                    "Já existe um procedimento com essa descrição!"
                )
                return

        profissional = (
            self.__controlador_principal
            .controlador_profissional
            .selecionar_profissional_para_procedimento()
        )

        if profissional is None:
            self.__tela_procedimento.mostrar_msg(
                "ERRO: É necessário vincular um profissional válido!"
            )
            return

        novo_procedimento = Procedimento(
            dados_proc["descricao"],
            dados_proc["custo"],
            profissional
        )

        self.__procedimentos.append(novo_procedimento)
        self.__tela_procedimento.mostrar_msg(
            "Procedimento cadastrado com sucesso!"
        )

    def alterar_procedimento(self):
        nome_busca = self.__tela_procedimento.selecionar()

        for proc in self.__procedimentos:
            if proc.descricao.lower() == nome_busca.lower():
                dados_proc = self.__tela_procedimento.pegar_dados()

                if dados_proc["descricao"].lower() != proc.descricao.lower():
                    for outro_proc in self.__procedimentos:
                        if (outro_proc.descricao.lower() ==
                                dados_proc["descricao"].lower()):
                            self.__tela_procedimento.mostrar_msg(
                                "ERRO: Já existe outro procedimento "
                                "com essa nova descrição!"
                            )
                            return

                proc.descricao = dados_proc["descricao"]
                proc.custo = dados_proc["custo"]

                novo_prof = (
                    self.__controlador_principal
                    .controlador_profissional
                    .selecionar_profissional_para_procedimento()
                )
                if novo_prof is not None:
                    proc.profissional = novo_prof

                self.__tela_procedimento.mostrar_msg(
                    "Procedimento alterado com sucesso!"
                )
                return

        self.__tela_procedimento.mostrar_msg(
            "ERRO: Não existe um procedimento com essa descrição!"
        )

    def excluir_procedimento(self):
        nome_busca = self.__tela_procedimento.selecionar()

        for proc in self.__procedimentos:
            if proc.descricao.lower() == nome_busca.lower():
                self.__procedimentos.remove(proc)
                self.__tela_procedimento.mostrar_msg(
                    "Procedimento excluído com sucesso!"
                )
                return

        self.__tela_procedimento.mostrar_msg(
            "ERRO: Não existe um procedimento com essa descrição!"
        )

    def listar_procedimentos(self):
        if len(self.__procedimentos) == 0:
            self.__tela_procedimento.mostrar_msg(
                "Nenhum procedimento cadastrado até o momento!"
            )
            return

        for proc in self.__procedimentos:
            dados = {
                "descricao": proc.descricao,
                "custo": proc.custo,
                "profissional_nome": proc.profissional.nome
            }
            self.__tela_procedimento.mostrar_procedimento(dados)

    def abrir_tela(self):
        lista_opcoes = {
            1: self.incluir_procedimento,
            2: self.alterar_procedimento,
            3: self.excluir_procedimento,
            4: self.listar_procedimentos,
            0: self.voltar
        }

        while True:
            opcao_escolhida = self.__tela_procedimento.mostrar_menu()
            if opcao_escolhida in lista_opcoes:
                funcao_escolhida = lista_opcoes[opcao_escolhida]
                funcao_escolhida()
            if opcao_escolhida == 0:
                break

    def voltar(self):
        return