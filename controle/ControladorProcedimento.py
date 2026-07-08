from entidade.procedimento import Procedimento
from limite_gui.TelaProcedimentoGUI import TelaProcedimentoGUI
from dao.ProcedimentoDAO import ProcedimentoDAO

class ControladorProcedimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__procedimento_dao = ProcedimentoDAO()
        self.__tela_procedimento = TelaProcedimentoGUI(self)

    @property
    def procedimentos(self):
        return self.__procedimento_dao.get_all()

    def iniciar(self):
        self.abrir_tela()

    def selecionar_procedimento_para_atendimento(self):
        procedimentos = self.__procedimento_dao.get_all()

        if not procedimentos:
            self.__tela_procedimento.mostrar_mensagem("ERRO: Nenhum procedimento cadastrado!")
            return None

        descricao = self.__tela_procedimento.tabela_procedimentos(procedimentos, selecionar=True)

        procedimento_selecionado = self.__procedimento_dao.get(descricao)

        if procedimento_selecionado is None:
            self.__tela_procedimento.mostrar_mensagem("ERRO: Procedimento não encontrado!")
            return None

        return procedimento_selecionado
    
    def remover_procedimentos_do_atendimento(self, atendimento) -> None:
        descricao = self.__tela_procedimento.tabela_procedimentos(atendimento.procedimentos, selecionar=True)
        
        for p in atendimento.procedimentos:
            if p.descricao == descricao:
                atendimento.procedimentos.remove(p)
                self.__controlador_principal.controlador_atendimento.atualizar_atendimento_dao(atendimento)
                self.__tela_procedimento.mostrar_mensagem("Procedimento removido do atendimento!")
                return
        
        self.__tela_procedimento.mostrar_mensagem("Procedimento não encontrado neste atendimento.")

    def incluir_procedimento(self):
        dados_procedimento = self.__tela_procedimento.abrir_janela_cadastro()

        if dados_procedimento is None:
            return

        if self.__procedimento_dao.get(dados_procedimento["descricao"]) is not None:
            self.__tela_procedimento.mostrar_mensagem("Já existe um procedimento com essa descrição!")
            return

        profissional = self.__controlador_principal.controlador_profissional.selecionar_profissional_para_procedimento()
        if profissional is None:
            return

        novo_procedimento = Procedimento(
            dados_procedimento["descricao"],
            dados_procedimento["custo"],
            profissional
        )

        self.__procedimento_dao.add(novo_procedimento)
        self.__tela_procedimento.mostrar_mensagem("Procedimento cadastrado com sucesso!")

    def alterar_procedimento(self):
        procedimentos = self.__procedimento_dao.get_all()
        if not procedimentos:
            self.__tela_procedimento.mostrar_mensagem("Nenhum procedimento cadastrado.")
            return

        descricao_busca = self.__tela_procedimento.tabela_procedimentos(procedimentos, selecionar=True)
        if descricao_busca is None:
            return

        procedimento = self.__procedimento_dao.get(descricao_busca)

        dados_atuais = {
            "descricao": procedimento.descricao,
            "custo": procedimento.custo
        }

        dados_novos = self.__tela_procedimento.abrir_janela_cadastro(dados_antigos=dados_atuais)
        if dados_novos is None:
            return

        if dados_novos["descricao"] != descricao_busca:
            self.__procedimento_dao.remove(descricao_busca)

        procedimento.descricao = dados_novos["descricao"]
        procedimento.custo = dados_novos["custo"]

        self.__procedimento_dao.update(procedimento)
        self.__tela_procedimento.mostrar_mensagem("Procedimento alterado com sucesso!")

    def excluir_procedimento(self):
        procedimentos = self.__procedimento_dao.get_all()
        if not procedimentos:
            self.__tela_procedimento.mostrar_mensagem("Nenhum procedimento cadastrado.")
            return

        descricao_busca = self.__tela_procedimento.tabela_procedimentos(procedimentos, selecionar=True)
        if descricao_busca is None:
            return

        self.__procedimento_dao.remove(descricao_busca)
        self.__tela_procedimento.mostrar_mensagem("Procedimento excluído!")

    def listar_procedimentos(self):
        procedimentos = self.__procedimento_dao.get_all()
        if not procedimentos:
            self.__tela_procedimento.mostrar_mensagem("Nenhum procedimento cadastrado!")
            return

        self.__tela_procedimento.tabela_procedimentos(procedimentos, selecionar=False)

    def abrir_tela(self) -> None:
        while True:
            opcao = self.__tela_procedimento.mostrar_menu()
            if opcao == "Incluir Procedimento":
                self.incluir_procedimento()
            
            elif opcao == "Alterar Procedimento":
                self.alterar_procedimento()
            
            elif opcao == "Excluir Procedimento":
                self.excluir_procedimento()

            elif opcao == "Listar Procedimentos":
                self.listar_procedimentos()
            
            elif opcao == "Voltar":
                break

    def voltar(self):
        return
