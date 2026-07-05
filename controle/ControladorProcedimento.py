from entidade.procedimento import Procedimento
from limite.TelaProcedimento import TelaProcedimento
from dao.ProcedimentoDAO import ProcedimentoDAO

class ControladorProcedimento:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__procedimento_dao = ProcedimentoDAO()
        self.__tela_procedimento = TelaProcedimento(self)

    def iniciar(self):
        self.abrir_tela()

    def selecionar_procedimento_para_atendimento(self):
        procedimentos = self.__procedimento_dao.get_all()

        if not procedimentos:
            self.__tela_procedimento.mostrar_msg("ERRO: Nenhum procedimento cadastrado!")
            return None

        self.__tela_procedimento.mostrar_lista(procedimentos) 
        descricao = self.__tela_procedimento.selecionar_procedimento()

        procedimento_selecionado = self.__procedimento_dao.get(descricao)

        if procedimento_selecionado is None:
            self.__tela_procedimento.mostrar_msg("ERRO: Procedimento não encontrado!")
            return None

        return procedimento_selecionado
    
    def remover_procedimentos_do_atendimento(self, atendimento) -> None:
        descricao = self.__tela_procedimento.selecionar_procedimento_para_remover(atendimento.procedimentos)
        
        for p in atendimento.procedimentos:
            if p.descricao == descricao:
                atendimento.procedimentos.remove(p)
                self.__controlador_principal.controlador_atendimento.atualizar_atendimento_dao(atendimento)
                self.__tela_procedimento.mostrar_msg("Procedimento removido do atendimento!")
                return
        
        self.__tela_procedimento.mostrar_msg("Procedimento não encontrado neste atendimento.")

    def incluir_procedimento(self):
        dados_procedimento = self.__tela_procedimento.pegar_dados()

        if self.__procedimento_dao.get(dados_procedimento["descricao"]) is not None:
            self.__tela_procedimento.mostrar_msg("Já existe um procedimento com essa descrição!")
            return

        profissional = (
            self.__controlador_principal
            .controlador_profissional
            .selecionar_profissional_para_procedimento()
        )

        if profissional is None:
            self.__tela_procedimento.mostrar_msg("ERRO: Profissional inválido!")
            return

        novo_procedimento = Procedimento(
            dados_procedimento["descricao"],
            dados_procedimento["custo"],
            profissional
        )

        self.__procedimento_dao.add(novo_procedimento)
        self.__tela_procedimento.mostrar_msg("Procedimento cadastrado com sucesso!")

    def alterar_procedimento(self):
        nome_busca = self.__tela_procedimento.selecionar()
        procedimento = self.__procedimento_dao.get(nome_busca)

        if procedimento is None:
            self.__tela_procedimento.mostrar_msg("ERRO: Procedimento não encontrado!")
            return

        dados_novos = self.__tela_procedimento.pegar_dados()

        if dados_novos["descricao"] != nome_busca:
            self.__procedimento_dao.remove(nome_busca)

        procedimento.descricao = dados_novos["descricao"]
        procedimento.custo = dados_novos["custo"]

        self.__procedimento_dao.add(procedimento)
        self.__tela_procedimento.mostrar_msg("Procedimento alterado com sucesso!")

    def excluir_procedimento(self):
        nome_busca = self.__tela_procedimento.selecionar()
        
        if self.__procedimento_dao.get(nome_busca) is not None:
            self.__procedimento_dao.remove(nome_busca)
            self.__tela_procedimento.mostrar_msg("Procedimento excluído!")
        else:
            self.__tela_procedimento.mostrar_msg("ERRO: Procedimento não encontrado!")

    def listar_procedimentos(self):
        procedimentos = self.__procedimento_dao.get_all()
        if not procedimentos:
            self.__tela_procedimento.mostrar_msg("Nenhum procedimento cadastrado!")
            return

        for p in procedimentos:
            self.__tela_procedimento.mostrar_procedimento({
                "descricao": p.descricao,
                "custo": p.custo,
                "profissional_nome": p.profissional.nome
            })

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